def main(args):
    print('ds locator starts')
    #argv = parse_arguments(['-o', 'https://sce-bio-c03486.ed.ac.uk', '-u', 'test', '-p', 'test', '-i', 'localhost', '-a', 'postgres', '-l', 'ds_locations'])
    argv = parse_arguments(args)
    print(argv)


if __name__ == "__main__":
   main(sys.argv[1:])