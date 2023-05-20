import os
import time
import shutil
import tempfile
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
        print("Session expired loging again")
        o.login(login, password)
        print("Logged in")

    return o


def get_datasets_page(o: Openbis, page = 0, page_size = 40):

    return o.get_datasets(props=['$NAME'], start_with=page * page_size, count=page_size)


def inspect_dataset(dataset: DataSet):
    print("{} {}".format(dataset.permId,dataset.props['$name']))
    print(dataset.attrs)
    #print("S{} {}".format(dataset.sample.code, dataset.sample.props['$name']))
    #print("E{} {}".format(dataset.experiment.permId, dataset.sample.props.get('$NAME')))


def out_data_frame():
    columns = ['SampleId','SampleCode', 'SampleName','ExperimentId','ExperimentCode', 'ExperimentName',
               'DataSetId','DataSetName','DataSetLocation','DataSetFiles']
    return pd.DataFrame(columns=columns)



def dataset_to_row(dataset: DataSet, locations:pd.DataFrame):

    location = 'missing'
    try:
        location = locations.loc[dataset.permId]['DataSetLocation']
    except KeyError:
        location = 'missing'

    files = ''
    try:
        files = ', '.join(dataset.file_list)
    except ValueError as E:
        print("Cannot get files for {}: {}".format(dataset.permId, E))

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
        row.update( {
            'ExperimentId': dataset.experiment.permId,
            # Code stored as an attribute dataset.attrs.experiment  but with space path
            'ExperimentCode': dataset.experiment.code,
            'ExperimentName': dataset.experiment.props['$name']
        })

    return pd.DataFrame(row, index=[0])



# do it

def get_datasets_locations_from_db(host,user,password,database="pathinfo_prod"):
    conn = psycopg2.connect(database=database, host=host, user=user, password=password)
    sql = "SELECT code, location FROM data_sets;"

    cursor = conn.cursor()
    cursor.execute(sql)
    resp = cursor.fetchall()
    df = pd.DataFrame(resp, columns =['DataSetId', 'DataSetLocation'])
    df = df.set_index('DataSetId', drop=False)
    conn.close()
    conn.close()
    return df


print("I started")


#conn = psycopg2.connect(database="pathinfo_prod", host="localhost", user="postgres")
#print(conn.status)

#sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
#sql = "SELECT code, location FROM data_sets;"

#cursor = conn.cursor()
#cursor.execute(sql)

#resp = cursor.fetchall()

#df = pd.DataFrame(resp, columns =['DataSetId', 'DataSetLocation'])
#df = df.set_index('DataSetId', drop=False)
#print(df)

#conn.close()

locations = get_datasets_locations_from_db(host="localhost", user="postgres", password=None)

o = connect_to_openbis(url='https://sce-bio-c03486.ed.ac.uk', login='test', password='test')

page = 0
page_size = 20
page_left = True

df = out_data_frame()

while page_left:
    datasets = get_datasets_page(o, page=page, page_size=page_size)
    page += 1
    page_left = len(datasets) > 0
    #print(len(datasets))


    rows = [df]
    for dataset in datasets:
        #inspect_dataset(dataset)
        dr = dataset_to_row(dataset,locations)
        #print(dr.to_string())
        rows.append(dr)

    df = pd.concat(rows)

df = df.set_index('DataSetId', drop=False)


#for id, row in df.iterrows():
#    print(id)
#    print(row)
# print(df.to_string())

missing = df.loc[df['DataSetLocation'] == 'missing']
if len(missing) > 0:
    print("Missing locations for datasets")
    print(missing['DataSetId'].to_string(index=False))

print("Located {} datasets, missing {}".format(len(df)-len(missing),len(missing)))
df.to_csv('datasets-locations-{}.csv'.format(datetime.today().strftime('%Y-%m-%d')))





