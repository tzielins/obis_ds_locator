import os
import sys
import time
import shutil
import tempfile
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import psycopg2

from pybis import Openbis, DataSet


def connect_to_openbis(url='', verify_certificates=False, token=None, login=None, password=None):
    o = Openbis(url=url,
                verify_certificates=verify_certificates,
                token=token,
                allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True)

    if not o.is_session_active():
        if not login:
            raise ValueError('obis login is required')
        if not password:
            raise ValueError('obis password is required')
        o.login(login, password)

    return o


def get_datasets_page(o: Openbis, page=0, page_size=40):
    return o.get_datasets(props=['$NAME'], start_with=page * page_size, count=page_size)


def inspect_dataset(dataset: DataSet):
    print("{} {}".format(dataset.permId, dataset.props['$name']))
    print(dataset.attrs)
    # print("S{} {}".format(dataset.sample.code, dataset.sample.props['$name']))
    # print("E{} {}".format(dataset.experiment.permId, dataset.sample.props.get('$NAME')))


def out_data_frame():
    columns = ['SampleId', 'SampleCode', 'SampleName', 'ExperimentId', 'ExperimentCode', 'ExperimentName',
               'DataSetId', 'DataSetName', 'DataSetLocation', 'DataSetFiles']
    return pd.DataFrame(columns=columns)


def dataset_to_row(dataset: DataSet, locations: pd.DataFrame, out=sys.stderr):
    location = 'missing'
    try:
        location = locations.loc[dataset.permId]['DataSetLocation']
    except KeyError:
        location = 'missing'

    files = ''
    try:
        files = ', '.join(dataset.file_list)
    except ValueError as E:
        print("Cannot get files for {}: {}".format(dataset.permId, E), file=out)

    row = {
        'DataSetId': dataset.permId,
        'DataSetName': dataset.props['$name'],
        'DataSetLocation': location,
        'DataSetFiles': files
    }

    # Code stored as an attribute dataset.attrs.sample but with space path
    if dataset.attrs.sample:
        row.update({
            'SampleId': dataset.sample.permId,
            'SampleCode': dataset.sample.code,
            'SampleName': dataset.sample.props['$name']
        })

    if dataset.attrs.experiment:
        row.update({
            'ExperimentId': dataset.experiment.permId,
            # Code stored as an attribute dataset.attrs.experiment  but with space path
            'ExperimentCode': dataset.experiment.code,
            'ExperimentName': dataset.experiment.props['$name']
        })

    return pd.DataFrame(row, index=[0])


# do it

def get_datasets_locations_from_db(host, user, password, database="pathinfo_prod"):

    conn = psycopg2.connect(database=database, host=host, user=user, password=password)

    sql = "SELECT code, location FROM data_sets;"
    cursor = conn.cursor()
    cursor.execute(sql)
    resp = cursor.fetchall()
    df = pd.DataFrame(resp, columns=['DataSetId', 'DataSetLocation'])
    df = df.set_index('DataSetId', drop=False)
    conn.close()
    conn.close()
    return df


def get_datasets_metadata(locations: pd.DataFrame, argv):
    o = connect_to_openbis(url=argv.openbis, login=argv.user, password=argv.password)

    page = 0
    page_size = 50
    page_left = True

    df = out_data_frame()

    while page_left:
        datasets = get_datasets_page(o, page=page, page_size=page_size)
        page += 1
        page_left = len(datasets) > 0

        rows = [df]
        for dataset in datasets:
            # inspect_dataset(dataset)
            dr = dataset_to_row(dataset, locations)
            # print(dr.to_string())
            rows.append(dr)

        df = pd.concat(rows)

    df = df.set_index('DataSetId', drop=False)
    return df


def parse_arguments(args=None):
    parser = argparse.ArgumentParser(
        prog='obis_ds_locator',
        description="Maps physical locations of datasets folders and puts them in a table with basic information " \
                    "about datasets, samples and experiments."
    )

    parser.add_argument("-o", "--openbis", help="url of OpenBis instance", default="https://localhost")
    parser.add_argument("-p", "--password", help="OpenBIS password")
    parser.add_argument("-u", "--user", help="OpenBis User")
    parser.add_argument("-i", "--db_host", help="database server", default="localhost")
    parser.add_argument("-d", "--db_name", help="path info database name", default="pathinfo_prod")
    parser.add_argument("-a", "--db_user", help="database user", default="postgres")
    parser.add_argument("-s", "--db_password", help="database password")
    parser.add_argument("-l", "--location", help="path to output files location", default='ds_locations')

    if args:
        return parser.parse_args(args)
    else:
        return parser.parse_args()


def locate_datasets_info(argv):
    locations = get_datasets_locations_from_db(host=argv.db_host, user=argv.db_user, password=argv.db_password,
                                               database=argv.db_name)
    metadata = get_datasets_metadata(locations, argv)
    return metadata


def handle_missing(metadata: pd.DataFrame, print_id=True, out=sys.stderr):
    missing = metadata.loc[metadata['DataSetLocation'] == 'missing']
    missing_nr = len(missing)
    if missing_nr > 0:
        if print_id:
            print("Missing dataset ids", file=out)
            print(missing['DataSetId'].to_string(index=False), file=out)
    return missing_nr


def store_ds_metadata(metadata: pd.DataFrame, argv):
    dir = argv.location
    if not dir:
        dir = '../..'

    Path(dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(dir, 'datasets-locations-{}.csv'.format(datetime.today().strftime('%Y-%m-%d')))
    metadata.to_csv(path)
    return path


def locate_and_save(argv):
    metadata = locate_datasets_info(argv)
    missing = handle_missing(metadata)

    print("Located {} datasets, missing {}".format(len(metadata) - missing, missing))
    store_ds_metadata(metadata, argv)
