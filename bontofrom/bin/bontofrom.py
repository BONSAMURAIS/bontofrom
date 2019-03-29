#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert metadata and data to bonsai ontology

Usage:
  bontofrom-cli metadata exiobase -s SUPPLY_TABLE_FILE -u USE_TABLE_FILE [-m 100] -r RDF_PATH
  bontofrom-cli metadata upload

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s SUPPLY_TABLE_FILE
  -u USE_TABLE_FILE
  -m maximum number of rows to evaluate in exiobase files
  -r RDF_PATH path to the rdf folder from: https://github.com/BONSAMURAIS/rdf

"""
from docopt import docopt
from bontofrom.convert_exiobase import convert_exiobase
import sys
from datetime import datetime

import logging

def main():
    logging.basicConfig(filename="bontofrom.log", level=logging.INFO)
    try:
        args = docopt(__doc__, version='0.1')
        if args['metadata'] and args['exiobase'] :
            if args['-m']:
                limit = int(args['-m'])
            else:
                limit = -1
            start = datetime.now()
            logging.info("Started {}".format(start.isoformat()))
            convert_exiobase(args['-s'], args['-u'], limit, args['-r'])
            end = datetime.now()
            logging.info("Ended {}".format(start.isoformat()))
        else:
            print("Doing nothing")
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
