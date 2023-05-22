import argparse


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
    parser.add_argument("--log", help="path to log file location", default='locator.LOG')

    if args:
        return parser.parse_args(args)
    else:
        return parser.parse_args()
