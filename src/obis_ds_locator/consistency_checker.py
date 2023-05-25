import os
import argparse
import pandas as pd

def parse_arguments(args=None):
    parser = argparse.ArgumentParser(
        prog='consistency_checker',
        description="Checks if files actually exists in the datasets locations extracted from openbis by obis_ds_locator"
    )

    parser.add_argument("-s", "--store", help="Openbis DataServer storage directory", default="dss_store")
    parser.add_argument("-l", "--locations", help="Path to the file with datasets locations")
    parser.add_argument("-f", "--file", help="Path to the file with output table")

    if args:
        return parser.parse_args(args)
    else:
        return parser.parse_args()


def read_locations(file):
    if not os.path.isfile(file):
        raise ValueError("{} is not a file".format(file))

    locations = pd.read_csv(file)
    return locations


def dataset_file_path(dss_store, ds_location, file_name):
    return os.path.join(dss_store, 'store', '1', ds_location, file_name)



def check_files(store: str, ds_location: str, files_names: str):
    present = []
    missing = []

    for file_name in files_names.split(","):
        file_name = file_name.strip()
        file_path = dataset_file_path(store, ds_location, file_name)
        if os.path.isfile(file_path):
            present.append(file_name)
        else:
            missing.append(file_name)
    return present, missing

def out_data_frame():
    columns = ['DataSetId', 'Status', 'DataSetLocation', 'DataSetFiles', 'MissingFiles']
    return pd.DataFrame(columns=columns)

def out_row(ds_metadata, present, missing):
    row = {
        'DataSetId': ds_metadata['DataSetId'],
        'Status': 'OK' if len(missing) == 0 else 'missing',
        'DataSetLocation': ds_metadata['DataSetLocation'],
        'DataSetFiles': ", ".join(present),
        'MissingFiles': ", ".join(missing)
    }
    return row

def check():

    args = None
    #args = ['-s','/localdisk/data/openngs/test-docker-state/dss_store','-l', 'ds_locations/datasets-locations-2023-05-23.csv','-f', 'ds_locations_check.csv']
    argv = parse_arguments(args)
    print(argv)

    locations = read_locations(argv.locations)

    df = out_data_frame()
    incomplete_ds = []

    for index, ds_metadata in locations.iterrows():
        if not ds_metadata['DataSetLocation'] == 'missing':
            present, missing = check_files(argv.store,ds_metadata['DataSetLocation'],ds_metadata['DataSetFiles'])
            if len(missing) > 0:
                incomplete_ds.append(ds_metadata['DataSetId'])
            row = out_row(ds_metadata, present, missing)
            df = pd.concat([df, pd.DataFrame(row, index=[0])])

    if len(incomplete_ds) > 0:
        if argv.file:
            df.to_csv(argv.file, index=False)
        else:
            print(df.to_csv(index=False))
        print("\nMissing files in {} datasets".format(len(incomplete_ds)))
        print(incomplete_ds)
    else:
        print("All datasets files accounted for")

if __name__ == "__main__":
    check()

