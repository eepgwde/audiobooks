#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Create an audiobook with chapters from files given as input.

Usage:
  audiobooks (-h | --help)
  audiobooks [-o FILE] [options] (--files FILE | <input>...)

Arguments:
  input                                 A directory of files or a file to update or 
                                        a glob pattern

Options:
  -h, --help                            Display help message.
  -l, --log                             Enable gmusicapi logging.
  -d, --dry-run                         Output options and files
  -q, --quiet                           Don't output status messages.
  --tmp DIR                             Pass this directory to use for 
                                        temporary files (otherwise use TMPDIR and then TMP)
  -o, FILE, --output FILE               Output .m4b file. Default: output.m4b
  --sort                                Sort tracks by disc and track number 
  -v, --verbose                         Output status messages.
                                        With -l,--log will display warnings.
                                        With -d,--dry-run will show parameters.
  -f FILE, --files FILE                 File containing files.
  --cover FILE                          Add a file of cover-art. Default: cover.jpg
  -c COMMAND, --command COMMAND         What to do: remove,write,cover,chapters

Patterns can be any valid Python regex patterns.

Commands:

 remove will remove any pre-existing file with the output filename
 write combines the .m4a files into one the output file using MP4Box
 cover will install the image file into the output M4B file
 chapters will install a chapter menu into the file
 quicktime will convert chapters to the QuickTime format

 chapters0 will print out the chapters entries to the console

Note:

 If you don't have MP4Box installed, you can get a chapter list with the command
 of chapters0.

"""

from __future__ import print_function;

import re
import csv
import os
import sys
import glob
import subprocess
import logging
import argparse

from math import floor
from unidecode import unidecode

from operator import attrgetter
from tempfile import mkstemp

import importlib.resources

from audiobooks._Book import Book

from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import MP4Cover, MP4
from mutagen.mp4 import AtomDataType
from mutagen.easymp4 import EasyMP4


QUIET = 25
logging.addLevelName(25, "QUIET")
logging.basicConfig(filename='audlibroj.log', level=QUIET)
global logger
logger = logging.getLogger(__name__)

def help0():
    """Prints the help message from the package."""
    try:
        help_content = importlib.resources.files("pitono.audio").joinpath("audlibroj.txt").read_text()
        print(help_content, file=sys.stderr)
    except FileNotFoundError:
        print("Help file not found.")


def parse_args():
  """
  Parses command-line arguments using argparse.

  Returns:
    Namespace: An object containing the parsed arguments.
  """
  parser = argparse.ArgumentParser(description="Process command-line arguments.")
  parser.add_argument(
    "-n", "--nodo", help="Enable/Disable nodo mode", action="store_true"
  )
  parser.add_argument(
    "-a", "--hashes", help="Use a file of hashes", action="store_true"
  )
  parser.add_argument(
    "-v", "--verbose", help="Display runtime messages", action="store_true"
  )
  parser.add_argument(
    "-f", "--input-file", required=True, help="Path to the input file"
  )
  parser.add_argument(
    "-o", "--output-file", required=False, help="Path to the output file"
  )

  args = parser.parse_args()

  # Check if input file exists
  if not os.path.isfile(args.input_file):
    parser.error(f"Input file '{args.input_file}' does not exist.")

  return args


def main():
    args = parse_args()
    args.prog = sys.argv[0]

    if args.nodo:
        help0()
    
    enable_logging = cli['log']
    if cli['quiet']:
        logger.setLevel(QUIET)
    else:
        logger.setLevel(logging.INFO)

    if enable_logging:
        logger.setLevel(logging.DEBUG)
        if cli['verbose']:
            sh = logging.StreamHandler()
            logger.addHandler(sh)
        logger.debug('cli: ' + type(cli).__name__)

    book = Book(**cli)
    
    if book is None:
        raise RuntimeError('no book')

    default0 = lambda x, d: d if x is None else x

    if cli['tmp'] is None:
        cli['tmp'] = os.environ['TMPDIR'] if os.environ.get('TMPDIR') else cli['tmp']
        if cli['tmp'] is None:
            cli['tmp'] = os.environ['TMP'] if os.environ.get('TMP') else cli['tmp']
        
    command1 = "chapters"
    command0 = default0(cli['command'], command1)
    command0 = command0.split(',')
    
    logger.info('book: ' + type(book).__name__)
    logger.info('book: ' + str(book))
    logger.info('book: commands: ' + "; ".join(command0))

    for cmd in command0:
        logger.info('cmd: ' + cmd + "; " +type(cmd).__name__ )
        r0 = book.__getattribute__(cmd)()
        if r0 is not None: 
            if isinstance(r0, list):
                print(*r0, sep='')

def audlibroj(*args, **kwargs): 
  main()

if __name__ == "__main__":
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(audlibroj())
