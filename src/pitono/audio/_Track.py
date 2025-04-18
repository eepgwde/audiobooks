## @file _Track.py
# @author weaves
# @brief An MP4 track.
#
# Holds a track.

import logging
from mutagen.easymp4 import EasyMP4
from functools import cached_property
from unidecode import unidecode

from math import floor
from pitono.weaves import TimeOps

logger = logging.getLogger("Test")


class Track(object):
  """single audio file"""

  _quality0 = None

  def __init__(self, fname):
    self._track = EasyMP4(fname)
    logger.info("Track: ctr: " + type(self._track).__name__)

  @cached_property
  def duration(self):
    """get track duration in seconds"""
    track_duration = int(floor(self._track.info.length) + 1)
    return track_duration

  @cached_property
  def duration1(self):
    """get track duration as a time"""
    t0 = self._track.info.length
    dt = TimeOps.instance().dtadvance2(seconds=t0)
    return dt.time()

  @cached_property
  def title(self):
    """get track title as unicode string"""
    track_title = "Unknown"
    try:
      track_title = self._track["title"][0]
    except:
      logger.warning("track_title")
    return track_title

  @cached_property
  def disc_track(self):
    """get disc and track number as tuple"""
    discnumber = 1
    try:
      discnumber = int(self._track["discnumber"][0])
    except:
      logger.warning("discnumber")

    tracknumber = 1
    try:
      tracknumber = int(self._track["tracknumber"][0])
    except:
      logger.warning("tracknumber")

    return (discnumber, tracknumber)

  @cached_property
  def album(self):
    """get album name"""
    track_album = self._track["album"][0]
    return track_album

  @property
  def filename(self):
    """get underlying filename"""
    return getattr(self._track, "filename")

  @cached_property
  def artist(self):
    """get artist name"""
    track_artist = self._track["artist"][0]
    return track_artist

  @property
  def quality0(self):
    """
    Set by a collection object.
    """
    return self._quality0

  @quality0.setter
  def quality0(self, val):
    self._quality0 = val

  def __lt__(self, other):
    logger.warning("lt: ")
    return self.disc_track < other.disc_track

  def __unicode__(self):
    """text representation"""
    return "<Track '%s'>" % self.title

  def __str__(self):
    """text representation"""
    return "<Disc {1:d} Track {2:d} '{0:s}'>".format(
      unidecode(self.title), self.disc_track[0], self.disc_track[1]
    )

  def __repr__(self):
    """utf-8 formatted text representation"""
    return self.__unicode__().encode("utf-8")
