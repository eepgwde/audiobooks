# -*- coding: utf-8 -*-
## @author weaves
##
## Container class for Tracks forming an AudioBook.

import logging
from unidecode import unidecode

import glob
import os

from cached_property import cached_property

from weaves import singledispatch1, Singleton

from audiobooks._Tracks import Tracks

logger = logging.getLogger('Test')

class Book(object):

  _chapters = []
  tracks = None

  CHAPTER_TEMPLATE = """CHAPTER{0:d}={1:s}
CHAPTER{0:d}NAME={2:s}
"""
  MERGE_COMMAND = "MP4Box"
  CHAPS_COMMAND = "mp4chaps"

  """
  List of audio filenames or a directory string is passed.
  Use the lookback.
  """
  def __init__(self, fnames, sort0=False):
    self.fnames = fnames
    self.tracks = Tracks(fnames, sort0 = sort0)

  def __repr__(self):
    """utf-8 formatted text representation"""
    return str(self.tracks)

  def chapters(self, file0=None):
    """Generate chapter marks and write to filename is given."""
    lines = []
    for track_number, track in enumerate(self.tracks):
      tm0 = Singleton.instance().dt2tm1(track.quality0)
      s0 = self.CHAPTER_TEMPLATE.format \
(track_number + 1, tm0, unidecode(track.title))
      lines.append(s0)

    if file0 is not None:
      with open(file0, 'w') as file1:
        file1.writelines(lines)

    return lines
