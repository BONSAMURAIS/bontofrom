#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generic executable.

This documentation defines how the program is run; see http://docopt.org/.

Commands:

Usage:

Options:

"""
from docopt import docopt
from bontofrom.worker import run
import sys


def main():
    try:
        args = docopt(__doc__, version='0.1')
        run(args)
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
