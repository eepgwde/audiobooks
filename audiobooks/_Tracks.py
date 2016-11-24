# -*- coding: utf-8 -*-
## @author weaves
##
## Container class for Track.

import logging

import glob
import os

from mutagen.easymp4 import EasyMP4
from cached_property import cached_property

from collections import UserList
from operator import attrgetter

from weaves import singledispatch1, Singleton

from audiobooks._Track import Track

logger = logging.getLogger('Test')

class Tracks(UserList):

  fnames = []
  _dt = None                    # the cumulative date.
  _cum0 = []                    # the cumulative times.

  """List of audio"""
  def __init__(self, fnames, sort0=False):
    super().__init__(self.load(fnames, sort0=sort0))
    self.fnames = fnames

  @singledispatch1
  def load(self, a):
    raise NotImplementedError('Unsupported type')
  
  @load.register(list)
  def _(self, fnames, sort0 = False):
    l0 = [Track(track_file) for track_file in fnames]
    if sort0:
      l0.sort()
    return l0
  
  @load.register(str)
  def _(self, dir0, sort0 = True):
    l0 = glob.glob(os.path.join(dir0, '*.m4a'))
    return self.load(l0, sort0=sort0)

  def __iter__(self):
    s0 = super().__iter__()
    logger.debug("Tracks: iter")
    self._cum0 = []
    self._dt = None
    return s0

  def __getitem__(self, i): 
    tr = super().__getitem__(i)
    logger.debug("Tracks: next")
    self.duration1(tr)
    return tr

  def duration1(self, tr):
    """
    This accumulates the time collected by duration()
    """
    tm = tr.duration1
    if self._dt is None:
      self._dt = Singleton.instance().tm2dt(tm)
    else:
      self._dt = Singleton.instance().dtadvance(self._dt, tm)

    self._cum0.append(Singleton.instance().dt2tm1(self._dt))
    return self._cum0[-1]

  def get(self, l0 = -1):
    return self._cum0[l0]

  def __repr__(self):
    """utf-8 formatted text representation"""
    return "; ".join( [str(x) for x in self.data] )
