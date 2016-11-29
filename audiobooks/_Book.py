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
  output0 = None
  cover0 = None

  CHAPTER_TEMPLATE = """CHAPTER{0:d}={1:s}
CHAPTER{0:d}NAME={2:s}
"""
  MERGE_COMMAND = "MP4Box"
  CHAPS_COMMAND = "mp4chaps"

  """
  List of audio filenames or a directory string is passed.
  Use the lookback.
  """
  def __init__(self, fnames, **kwargs):
    self.fnames = fnames
    sort0 = kwargs.get('sort0', False)
    self.tracks = Tracks(fnames, sort0 = sort0)

    output0 = kwargs.get('output0', None)
    if output0 is None:
      try:
        output0 = "{:s}.m4b".format(unidecode(self[0].album))
      except:
        output0 = "output.m4b"
        logger.warning("Book: ctr: failed: output")
    self.output0 = output0

    cover0 = kwargs.get('cover0', None)
    if cover0 is None:
      try:
        cover0 = "{:s}.jpg".format(unidecode(self[0].album))
      except:
        cover0 = "cover.jpg"
        logger.warning("Book: ctr: failed: cover")
    self.cover0 = cover0

  def __repr__(self):
    """utf-8 formatted text representation"""
    default0 = lambda x,d: d if x is None else x
    
    s0 = "\"{0:s}\" \"{1:s}\"".format \
(default0(self.output0, ""), default0(self.cover0, ""))
    return "( {0:s} : {1:s} )".format(s0, str(self.tracks))

  def __getitem__(self, i): 
    return self.tracks[i]

  def __len__(self): 
    return len(self.tracks)

  def chapters(self):
    """
    Generate chapter marks and write to filename is given.
    @note
    cached_property cannot be called using getattribute.
    """
    lines = []
    for track_number, track in enumerate(self.tracks):
      tm0 = Singleton.instance().dt2tm1(track.quality0)
      s0 = self.CHAPTER_TEMPLATE.format \
(track_number + 1, tm0, unidecode(track.title))
      lines.append(s0)
    return lines

  def write(self):
    return

  
