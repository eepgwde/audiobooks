# -*- coding: utf-8 -*-
## @author weaves
##
## Container class for Tracks forming an AudioBook.

import logging

import glob
import os

from cached_property import cached_property

from weaves import singledispatch1, Singleton

from audiobooks._Tracks import Tracks

logger = logging.getLogger('Test')

class Book(object):

  _chapters = []
  tracks = None

  """List of audio"""
  def __init__(self, fnames, sort0=False):
    self.fnames = fnames
    self.tracks = Tracks(fnames, sort0 = sort0)

  def __repr__(self):
    """utf-8 formatted text representation"""
    return str(self.tracks)

