import sys
import time

from obis_ds_locator import parse_arguments, locate_and_save

def main():
    start_time = time.time()
    print("ds locator starts {}".format(start_time))
    argv = parse_arguments()

    # -o https://sce-bio-c03486.ed.ac.uk -u test -p test -i localhost -a postgres -l ds_locations
    #argv = parse_arguments(['-o', 'https://sce-bio-c03486.ed.ac.uk', '-u', 'test', '-p', 'test', '-i', 'localhost', '-a', 'postgres', '-l', 'ds_locations'])
    #print(argv)
    locate_and_save(argv)
    duration = (time.time() - start_time)
    print("Finished after {} minutes".format(duration % 60))

if __name__ == "__main__":
    main()

