import time, sys
import logging

from obis_ds_locator import locate_and_save, parse_arguments

def main():

    start_time = time.time()
    argv = parse_arguments()

    logging.basicConfig(filename=argv.log, level=logging.INFO, format='%(asctime)s - %(message)s')
    # print("ds locator starts")
    logging.info("dataset locator starts")

    try:
        # -o https://sce-bio-c03486.ed.ac.uk -u test -p test -i localhost -a postgres -l ds_locations
        #argv = parse_arguments(['-o', 'https://sce-bio-c03486.ed.ac.uk', '-u', 'test', '-p', 'test', '-i', 'localhost', '-a', 'postgres', '-l', 'ds_locations'])
        #print(argv)

        locate_and_save(argv)
        duration = (time.time() - start_time) // 60
        # print("Finished after {} minutes".format(duration))
        logging.info("Finished after {} minutes".format(duration))
    except Exception as e:
        logging.error("Failed", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

