#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert metadata and data to bonsai ontology

Usage:
  bontofrom-cli metadata exiobase
  bontofrom-cli metadata upload

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from bontofrom.convert_metadata import convert_exiobase
# from bontofrom.worker import run
import sys


def main():
    try:
        args = docopt(__doc__, version='0.1')
        if args['metadata'] and args['exiobase']:
            convert_exiobase()
        else:
            print("Doing nothing")
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
