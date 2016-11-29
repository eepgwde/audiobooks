# -*- coding: utf-8 -*-
## @author weaves
##
## Container class for Track.

import logging

import glob
import os

import datetime

from mutagen.easymp4 import EasyMP4
from cached_property import cached_property

from collections import UserList
from operator import attrgetter

from weaves import singledispatch1, Singleton

from audiobooks._Track import Track

logger = logging.getLogger('Test')

class Tracks(UserList):

  fnames = []
  _dt = None                    # the quality0 date.
  _delegate = None

  def set_delegate(self, name0):
    self._delegate = getattr(self, name0)
    
  """List of audio"""
  def __init__(self, fnames, **kwargs):
    super().__init__(self.load(fnames, sort0=kwargs.get('sort', False)))
    self.set_delegate(kwargs.get('delegate0', "before"))
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
    tr.quality0 = self._delegate(tr)
    return tr

  def after(self, tr):
    """
    This accumulates the time collected by duration().
    This is time at the end of the track.
    """
    tm = tr.duration1
    if self._dt is None:
      self._dt = Singleton.instance().tm2dt(tm)
    else:
      self._dt = Singleton.instance().dtadvance(self._dt, tm)
    return self.get()

  def before(self, tr):
    """
    This accumulates the time collected by duration().
    This is time at the end of the track.
    """
    if self._dt is None:
      self._dt = Singleton.instance().epoch
    t0 = self.get()
    self.after(tr)
    return t0

  def get(self, l0 = -1):
    return self._dt

  def __repr__(self):
    """utf-8 formatted text representation"""
    return "; ".join( [str(x) for x in self.data] )

