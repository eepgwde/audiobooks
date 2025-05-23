"""
@author weaves

Container class for Tracks forming an AudioBook.

Be sure that the TMP directory is large enough.

"""

# -*- coding: utf-8 -*-

import logging
from unidecode import unidecode

import os
import subprocess

from tempfile import mkstemp, gettempdir
from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import MP4Cover, MP4
from mutagen.mp4 import AtomDataType

from pitono.weaves import TimeOps

from ._Tracks import Tracks

logger = logging.getLogger("Test")


class Book(object):
  _chapters = []
  tracks = None
  output0 = None
  cover0 = None
  nodo = False
  tmp = None

  CHAPTER_TEMPLATE = """CHAPTER{0:d}={1:s}
CHAPTER{0:d}NAME={2:s}
"""
  MERGE_COMMAND = "MP4Box"
  QT_COMMAND = "mp4chaps"

  def __init__(self, **kwargs):
    """Initialize an audiobook container. Accepts keys that are typically
    command-line arguments:
    - dry-run, boolean, do nothing if True
    - input, a list of files to include in the book;
    - sort, a boolean, should the files be sorted on disc and track number
    - files, a string for the path to a file that contains files
    - output, string, output filename
    - cover, string, source filename for an image
    """
    for k in kwargs.items():
      logger.info(k)

    self.nodo = kwargs.get("dry-run", False)

    default0 = lambda x, d: d if x is None else x

    self.tmp = kwargs.get("tmp", gettempdir())
    if self.tmp is None:
      self.tmp = os.environ.get("TMPDIR", "/tmp")
    logger.info(f"tmp: {self.tmp}")

    ## files is a file of filenames
    if "files" in kwargs and isinstance(kwargs["files"],str):
      x0 = kwargs["files"]
      with open(x0, encoding="utf-8") as f:
        files = f.read().splitlines()
        sort0 = kwargs.get("sort", False)
        self.tracks = Tracks(files, sort=sort0)
    elif "input" in kwargs and len(kwargs["input"]) > 0:
      ## input is a list
      self.tracks = Tracks(kwargs["input"], sort=kwargs.get("sort", False))
    else:
      logger.error("No files given")
      raise ValueError("No files given")

    output0 = kwargs.get("output", None)
    if output0 is None:
      try:
        output0 = "{:s}.m4b".format(unidecode(self[0].album))
      except Exception as e:
        output0 = "output.m4b"
        logger.warning("Book: ctr: failed: output")
    self.output0 = output0

    cover0 = kwargs.get("cover", None)
    if cover0 is None:
      try:
        cover0 = "{:s}.jpg".format(unidecode(self[0].album))
      except:
        cover0 = "cover.jpg"
        logger.warning("Book: ctr: failed: cover")
    self.cover0 = cover0

  def __repr__(self):
    """ASCII formatted text representation"""
    default0 = lambda x, d: d if x is None else unidecode(x)

    s0 = '"{0:s}" "{1:s}"'.format(
      default0(self.output0, ""), default0(self.cover0, "")
    )
    return "( {0:s} : {1:s} )".format(s0, str(self.tracks))

  def __getitem__(self, i):
    """Indexed access: return the track at the i-th position"""
    return self.tracks[i]

  def __len__(self):
    """The number of tracks"""
    return len(self.tracks)

  def _duration(self, track):
    """return the duration as a string for use."""
    dt0 = TimeOps.instance().tm2dt(track.duration1)
    tm0 = TimeOps.instance().dt2tm1(dt0)
    return tm0

  def _cumulative(self, track):
    """return the duration as a string for use."""
    tm0 = TimeOps.instance().dt2tm1(track.quality0)
    return tm0

  def chapters0(self):
    """
    Generate chapter marks and write to filename is given.
    @note
    cached_property cannot be called using getattribute.
    """
    lines = []
    for track_number, track in enumerate(self.tracks):
      tm0 = self._cumulative(track)
      s0 = self.CHAPTER_TEMPLATE.format(
        track_number + 1, tm0, unidecode(track.title)
      )
      lines.append(s0)
    self._chapters = lines
    return self._chapters

  def metadata(self, **kwargs):
    """Write album and artist information to audiobook file.

    Changes the filename, expects album and artist to be defined by the first track
    """
    if self.nodo:
      return

    track = EasyMP4(self.output0)
    track["album"] = kwargs.get("album", self[0].album)
    track["title"] = track["album"]
    track["artist"] = kwargs.get("artist", self[0].artist)
    track.save()

  def cover(self, **kwargs):
    """Write cover image to audiobook file"""
    self.cover0 = kwargs.get("cover", self.cover0)
    if self.cover0.endswith("png"):
      picture_type = AtomDataType.PNG
    elif self.cover0.endswith("jpg") or self.cover0.endswith("jpeg"):
      picture_type = AtomDataType.JPEG
    if self.nodo:
      return

    logger.debug("cover: " + self.cover0)
    with open(self.cover0, "rb") as file0:
      art0 = MP4Cover(data=file0.read(), imageformat=picture_type)
      track = MP4(self.output0)
      track["covr"] = [art0]
      track.save()

  def _invoke(self, cmd):
    merger1 = -1
    if self.nodo:
      logger.info("write: cmd: " + "; ".join(cmd))
    else:
      merger1 = subprocess.call(cmd)
    return merger1

  def write(self, **kwargs):
    """combine m4a files to one big file
    writes to the output file name, make sure files are encoded to same
    audio quality.

    Files are added one at a time - reduces memory footprint and use of
    TMP directory"""
    if len(self.tracks) <= 0:
      raise RuntimeError("no tracks")

    h0, *t0 = self.tracks

    tag = ""
    tag = "#audio"

    for t1 in self.tracks:
      merger0 = []
      merger0.insert(0, self.MERGE_COMMAND)
      merger0.append("-tmp")
      merger0.append(self.tmp)
      merger0.append("-cat")
      merger0.append("{0:s}{1:s}".format(t1.filename, tag))
      merger0.append(self.output0)
      self._invoke(merger0)

    return self.output0

  def chapters(self, **kwargs):
    """Attach a chapters menu to the file book.

    This will invoke chapters0() if necessary."""

    if len(self._chapters) <= 0:
      self.chapters0()
    if len(self._chapters) <= 0:
      raise RuntimeError("no chapters")

    fchaps = mkstemp(prefix="chaplist")[1]
    with open(fchaps, "w") as file0:
      file0.writelines(self._chapters)

    merger0 = []
    merger1 = -1
    merger0.insert(0, self.MERGE_COMMAND)
    merger0.extend(["-chap", fchaps])
    merger0.append(self.output0)
    if self.nodo:
      logger.info("write: cmd: " + "; ".join(merger0))
    else:
      merger1 = subprocess.call(merger0)
      if not self.nodo:
        os.remove(fchaps)
      if merger1 != 0:
        raise RuntimeError("Merge unsuccessful")
    return self.output0

  def quicktime(self, **kwargs):
    """Convert chapters to QuickTime."""

    merger0 = []
    merger1 = -1
    merger0.insert(0, self.QT_COMMAND)
    merger0.append("-c")
    merger0.append("-Q")
    merger0.append(self.output0)
    if self.nodo:
      logger.info("write: cmd: " + "; ".join(merger0))
    else:
      merger1 = subprocess.call(merger0)
      if merger1 != 0:
        raise RuntimeError("QuickTime chapters failed")
    return self.output0

  def remove(self, **kwargs):
    """Delete the output file"""
    try:
      if not self.nodo:
        os.remove(self.output0)
    except:
      logger.warning("remove: " + self.output0)
