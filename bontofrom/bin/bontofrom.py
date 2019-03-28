#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert metadata and data to bonsai ontology

Usage:
  bontofrom-cli metadata exiobase -s SUPPLY_TABLE_FILE -u USE_TABLE_FILE
  bontofrom-cli metadata upload

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s SUPPLY_TABLE_FILE
  -u USE_TABLE_FILE

"""
from docopt import docopt
from bontofrom.convert_exiobase import convert_exiobase
import sys


def main():
    try:
        args = docopt(__doc__, version='0.1')
        if args['metadata'] and args['exiobase']:
            convert_exiobase(args['-s'], args['-u'])
        else:
            print("Doing nothing")
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
