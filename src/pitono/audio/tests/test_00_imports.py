"""
Test file for the audio package.

Test the important imports. This should be run on both the development and the runtime environment.

"""

## @file Test.py
# @author weaves
# @brief Unittest
#
# @note
#
# Relatively complete test.

import sys, logging, os
from unidecode import unidecode
from mutagen.mp4 import MP4Cover, MP4
from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import AtomDataType

from pitono.weaves import TimeOps
from MediaInfoDLL3 import MediaInfo, Stream, Info

from datetime import datetime, timezone, timedelta, date

from collections import Counter
from operator import attrgetter
from pitono.weaves import singledispatch1, TimeOps

import unittest

from pitono.audio import Track, Tracks, Book
from pitono.audio import MInfo, MInfo1
from cached_property import cached_property

logfile = (
  os.environ["X_LOGFILE"] if os.environ.get("X_LOGFILE") is not None else "test.log"
)
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger("Test")
sh = logging.StreamHandler()
logger.addHandler(sh)

media0 = os.path.join(os.path.dirname(__file__), "media")
trs0 = os.path.join(os.path.dirname(__file__), "p1.lst")


class Test(unittest.TestCase):
  """
  A source directory dir0 is taken from the environment as SDIR or
  is tests/media and should contain .m4a files.
  A file tests/p1.lst is also needed. It can list the files in the
  directory.
  """

  test0 = None
  dir0 = None
  files0 = []
  files = []
  logger = None

  ## Sets pandas options and logging.
  @classmethod
  def setUpClass(cls):
    global logger
    cls.logger = logger
    global media0
    cls.dir0 = os.environ["SDIR"] if os.environ.get("SDIR") is not None else media0

    for root, dirs, files in os.walk(cls.dir0, topdown=True):
      for name in files:
        cls.files.append(os.path.join(root, name))

    cls.files.sort()
    cls.files0 = cls.files
    cls.logger.info("files: " + unidecode("; ".join(cls.files)))

  ## Logs out.
  @classmethod
  def tearDownClass(cls):
    pass

  ## Null setup. Create a new one.
  def setUp(self):
    self.logger.info("setup")
    if not type(self).files:
      type(self).files = type(self).files0

    self.assertTrue(len(self.files))

    self.file0, *type(self).files = type(self).files
    self.test0 = Track(self.file0)
    return

  ## Null setup.
  def tearDown(self):
    self.logger.info("tearDown")
    return

  ## Loaded?
  ## Is utf-8 available as a filesystemencoding()
  def test_000(self):
    self.assertIsNotNone(self.test0)
    return

