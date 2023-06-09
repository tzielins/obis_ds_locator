# OpenBIS datasets locator

Finds the physical locations of the datasets and
stores them in a log file.

## Setup

```
conda create -n ds-locations python=3.8
conda activate ds-locations
conda install -c anaconda psycopg2
# cause pip cannot install psycopg2 on its own

git clone https://github.com/tzielins/obis_ds_locator.git
cd obis_ds_locator/src
pip install .
```




## Usage
```
obis_ds_locator -h

obis_ds_locator -o https://obis-instance -u obis_user -p obis_password -d path_db_name -i db_host -a db_user -s db_pass -l out_locations

obis_ds_locator -u test -p test
# uses localhost defaults

```

There is also a module consistency_checker.py whic takes as input the locations
found by obis_ds_locator and checks if the listed files are actually present on the disk.

```
python obis_ds_locator/consistency_checker.py -s path-to-obisstorage -l path-to-datasets-locations.csv -f 'optional location of report file'
```
