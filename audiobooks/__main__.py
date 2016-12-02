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

from audiobooks._Book import Book

from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import MP4Cover, MP4
from mutagen.mp4 import AtomDataType
from mutagen.easymp4 import EasyMP4

from unidecode import unidecode
from docopt import docopt

import csv
import os
import sys
import glob
import subprocess

from math import floor
from operator import attrgetter
from tempfile import mkstemp

import logging

QUIET = 25
logging.addLevelName(25, "QUIET")
logging.basicConfig(filename='audiobooks.log', level=QUIET)
global logger
logger = logging.getLogger('Test')

def main():
    global cli
    global logger

    argv = sys.argv
    
    cli = dict((key.lstrip("-<").rstrip(">"), value) for key, value in docopt(__doc__).items())

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

