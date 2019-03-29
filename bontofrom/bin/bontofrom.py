#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert metadata and data to bonsai ontology

Usage:
  bontofrom-cli metadata exiobase -s SUPPLY_TABLE_FILE -u USE_TABLE_FILE [-l 100]
  bontofrom-cli metadata upload

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s SUPPLY_TABLE_FILE
  -u USE_TABLE_FILE
  -l max number of rows to evaluate in exiobase files

"""
from docopt import docopt
from bontofrom.convert_exiobase import convert_exiobase
import sys


def main():
    try:
        args = docopt(__doc__, version='0.1')
        if args['metadata'] and args['exiobase']:
            if args['-l']:
                limit = int(args['-l'])
            else:
                limit = -1
            convert_exiobase(args['-s'], args['-u'], limit)
        else:
            print("Doing nothing")
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
