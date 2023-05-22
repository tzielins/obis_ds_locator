# OpenBIS datasets locator

Finds the physical locations of the datasets and
stores them in a log file.

## Setup

```
conda install -c anaconda psycopg2
# cause pip cannot install psycopg2 on its own
```


cd src
pip install .

## Usage
```
obis_ds_locator -h

obis_ds_locator -o https://obis-instance -u obis_user -p obis_password -d path_db_name -i db_host -a db_user -s db_pass -l out_locations

obis_ds_locator -u test -p test
# uses localhost defaults

```


