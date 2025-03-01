## @file MInfo.py
# @brief Media Info fetching.
# @author weaves
#
# @details
# This class uses the MediaInfo library for Python.
#
# @note
#
# The library has a limitation that it cannot handle UTF-8 names very
# well. To side-step that, I make a temporary symlink using the 'os'
# module and then use MediaInfo on that.
#
#

from __future__ import print_function
from unidecode import unidecode

import logging

import sys


class MInfo(object):
  """
  Given a set of frequencies and a set of numbers provides
  a stream of randomly chosen numbers from the set with the given
  frequency.
  """

  _slv = None
  _logger = logging.getLogger("MInfo")

  quality0 = "Audio;%Duration/String3%"

  def __init__(self, l0=None):
    self._delegate = "duration1"

    self._slv = MediaInfo()
    self._logger.info(
      self._slv.Option_Static(
        "Info_Version", "0.7.7.0;MediaInfoDLL_Example_Python;0.7.7.0"
      )
    )
    if l0 == None:
      return

    if not isinstance(l0, str):
      return

    try:
      self.open(l0)
    except:
      raise

    return

  def dispose(self):
    """
    The media info has to be re-created for every file.
    """
    if self._slv is None:
      return
    self._slv.Close()
    return

  def open(self, *args, l0=None, **kwargs):
    """
    The mediainfo object has to be recreated every time.
    """
    if args:
      return self.open(l0=args[0])
    l1 = None
    try:
      self.dispose()
      if l0 == None:
        return
      self._slv = MediaInfo()

      self._logger.info("file: Open: " + unidecode(l0))
      self._slv.Open(l0)

    except:
      self._logger.warning(
        "file: Open: fail: "
        + unidecode(l0)
        + "; "
        + sys.exc_info()[0].__name__
        + "; "
        + sys.exc_info()[2]
        + "; "
        + "."
      )

    return

  def quality(self):
    """
    Hoping to obtain
    mediainfo --Inform='Audio;%Duration/String3%' media/01.The_best_is_yet_to_come.m4a
    """

    ## self._logger.info("quality: key: " + self.quality0)
    self._slv.Option_Static("Inform", self.quality0)
    self._logger.info("quality: " + self._slv.Inform())
    return self._slv.Inform()

  def info(self, l0=None):
    """ """
    self._slv.Option_Static("Complete", "1")
    return self._slv.Inform()
