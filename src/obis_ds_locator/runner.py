import sys
from obis_ds_locator import parse_arguments, locate_and_save

def main():
    print('ds locator starts')
    argv = parse_arguments()
    #print(argv)
    # -o https://sce-bio-c03486.ed.ac.uk -u test -p test -i localhost -a postgres -l ds_locations
    #argv = parse_arguments(['-o', 'https://sce-bio-c03486.ed.ac.uk', '-u', 'test', '-p', 'test', '-i', 'localhost', '-a', 'postgres', '-l', 'ds_locations'])
    #print(argv)
    locate_and_save(argv)


if __name__ == "__main__":
    main()

