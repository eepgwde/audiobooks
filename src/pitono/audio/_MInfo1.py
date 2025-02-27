# @file MInfo.py
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

from MediaInfoDLL3 import MediaInfo, Stream, Info

import logging
from datetime import datetime, date
from tempfile import NamedTemporaryFile

import os
import sys

from ._MInfo import MInfo

class MInfo1(MInfo):
    """
    Given a set of frequencies and a set of numbers provides
    a stream of randomly chosen numbers from the set with the given
    frequency.
    """
    # Values that may be returned by next_num()
    epoch = datetime.utcfromtimestamp(0)

    _cum0 = []
    _slv = None
    _hrfmt = "{0:02d}:{1:02d}:{2:02d}.{3:03d}"
    _dt = None
    _logger = logging.getLogger('MInfo')
    _loaded = False
    _delegate = None

    format0 = "%H:%M:%S.%f"
    format1 = "{1:s} Chapter_{0:d}"
    format10 = "{:s} Chapter"
    quality0 = "Audio;%Duration/String3%"

    null_tm = None

    def set_delegate(self, name0):
        self._delegate = getattr(self, name0)
    
    def __init__(self, **kwargs):
        super().__init__(l0 = kwargs.get('l0', None))
        self.null_tm = self.dt2tm1(self.epoch)
        self.set_delegate(kwargs.get('delegate0', "duration1"))

    def dispose(self):
        """
        Base class only
        """
        super().dispose()

    def duration(self):
        """
        If the quality string has been correctly set, this will collect a
        time string from the file using MediaInfo and format it as a
        time instance.
        """
        s0 = self.quality()
        if len(s0) <= 0:
            return None
        self._logger.debug("duration: s0: " + s0)
        d = datetime.strptime(s0, self.format0)
        return self.tm2dt(datetime.time(d))
        
    def duration1(self):
        """
        This accumulates the time collected by duration()
        """
        d = self.duration()
        if self._dt is None:
            self._dt = d
        else:
            self._dt = self.dtadvance(self._dt, datetime.time(d))

        self._cum0.append(self.dt2tm1(self._dt))

        return self._cum0[-1]

    def duration2(self):
        """
        Returns a list with a formatted string. If this is the initial call, then
        returns two strings within it.
        """
        r0 = []
        t0 = self.duration1()
        if len(self._cum0) == 1:
            r0 = [ self.format10.format(self.null_tm) ]

        if t0 is None:
            return r0
        s0 = self.format1.format(len(self._cum0), t0)
        r0.append(s0)
        self._logger.info('duration2: ' + str(len(r0)))
        return r0

    def next(self, l0):
        s0 = self._delegate()
        if l0 is not None:
            self.open(l0)
        return s0

    def get(self, l0 = -1):
        return self._cum0[l0]

    def reset(self, l0 = None):
        x0 = self._cum0
        self._cum0 = []
        self._dt = None
        return x0

    @classmethod
    def tm2dt(cls, tm):
        return datetime.combine(cls.epoch, tm)

    @classmethod
    def dtadvance(cls, dt, tm):
        return dt + (cls.tm2dt(tm) - cls.epoch)

    @classmethod
    def dofy(cls, d):
        """
        Day of year, indexed from zero.
        """
        return d.toordinal() - date(d.year, 1, 1).toordinal()

    @classmethod
    def dt2tm1(cls, d):
        hr0 = cls.dofy(d) * 24 + d.hour
        return cls._hrfmt.format(hr0, d.minute,
                                 d.second, int(d.microsecond / 1000))
