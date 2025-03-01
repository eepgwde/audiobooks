#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import os
import sys
import logging
import argparse

import importlib.resources

from pitono.audio import Book
import argparse

QUIET = 25
logging.addLevelName(25, "QUIET")
logging.basicConfig(filename="audlibroj.log", level=QUIET)
logger = logging.getLogger(__name__)


class ArgumentParser1(argparse.ArgumentParser):
  def print_help(self, file=None):
    if file is None:
      file = sys.stderr  # Default to standard error

    try:
      help_content = (
        importlib.resources.files("pitono.audio")
        .joinpath("audlibroj.txt")
        .read_text()
      )
      file.write(help_content)
    except FileNotFoundError:
      print("Help file not found.")


def parse_args():
  """
  Parses command-line arguments using argparse.

  Returns:
    Namespace: An object containing the parsed arguments.
  """
  parser = ArgumentParser1(description="Audiobook M4B creation")
  parser.add_argument("-l", "--log", action="store_true", help="Enable logging.")
  parser.add_argument("-n", "--dry-run", action="store_true", help="Dry-run do nothing.")
  parser.add_argument("-q", "--quiet", action="store_true", help="Don't output status messages.")
  parser.add_argument("--tmp", dest="tmp", help="Use this directory temporary files (otherwise use TMPDIR and then TMP).")
  parser.add_argument("-o", "--output", dest="output", help="Output file the M4B file. Default: <album>.m4b and if no album output.m4b")
  parser.add_argument("--sort", action="store_true", help="Sort tracks by disc and track number.")
  parser.add_argument("-v", "--verbose", action="store_true", help="Output status messages. With -l,--log will display warnings. With -n,--dry-run will show parameters.")
  parser.add_argument("-f", "--files", dest="files", help="Input file containing list of M4A .m4a files.")
  parser.add_argument("--cover", dest="cover", help="Add a file of cover-art. Default: <album>.jpg and then cover.jpg")
  parser.add_argument("-c", "--command", dest="command", help="What to do, comma-separated: remove, write, cover, chapters.")

  args, xargs = parser.parse_known_args()
  args.input = xargs

  # Check if input file exists
  if not os.path.isfile(args.files):
    parser.error(f"Input file '{args.files}' does not exist.")

  return args

  # # Access arguments:
  # log = args.log
  # dry_run = args.dry_run
  # quiet = args.quiet
  # tmp_dir = args.tmp_dir
  # output_file = args.output_file
  # sort = args.sort
  # verbose = args.verbose
  # files_file = args.files_file
  # cover_file = args.cover_file
  # command = args.command

def main():
  args = parse_args()
  args.prog = sys.argv[0]

  enable_logging = args.log
  if args.quiet:
    logger.setLevel(QUIET)
  else:
    if enable_logging:
      logger.setLevel(logging.DEBUG)
    else:
      logger.setLevel(logging.INFO)

  if args.verbose:
    sh = logging.StreamHandler()
    logger.addHandler(sh)

  logger.debug(f"args: {args}")

  # Convert args to a dictionary:
  cli = vars(args)
  logger.debug(f"cli: {cli}")

  book = Book(**cli)

  if book is None:
    raise RuntimeError("no book")

  default0 = lambda x, d: d if x is None else x

  if args.tmp is None:
    args.tmp = os.environ["TMPDIR"] if os.environ.get("TMPDIR") else args.tmp
    if args.tmp is None:
      args.tmp = os.environ["TMP"] if os.environ.get("TMP") else args.tmp

  command1 = "chapters"
  command0 = default0(args.command, command1)
  command0 = command0.split(",")

  logger.info("book: " + type(book).__name__)
  logger.info("book: " + str(book))
  logger.info("book: commands: " + "; ".join(command0))

  for cmd in command0:
    logger.info("cmd: " + cmd + "; " + type(cmd).__name__)
    r0 = book.__getattribute__(cmd)()
    if r0 is not None:
      if isinstance(r0, list):
        print(*r0, sep="")


def audlibroj(*args, **kwargs):
  main()


if __name__ == "__main__":
  sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
  sys.exit(audlibroj())
