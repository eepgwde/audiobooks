from mutagen.easymp4 import EasyMP4
from cached_property import cached_property

from collections import UserList

from weaves import singledispatch1

from audiobooks._Track import Track

class Tracks(UserList):

  fnames = []

  """List of audio"""
  def __init__(self, fnames):
    super().__init__(self.load(fnames))
    self.fnames = fnames

  def __iter__(self):
    return self

  def __next__(self):
    tr = self.tracks.next()
    return tr

  @singledispatch1
  def load(self, a):
    raise NotImplementedError('Unsupported type')
  
  @load.register(list)
  def _(self, fnames, sort0 = False):
    l0 = [Track(track_file) for track_file in fnames]
    if sort0:
      l0 = sorted(l0.items(), key=lambda t: attrgetter('disc_track'))
    return l0
  
  @load.register(str)
  def _(self, dir0, sort0 = True):
    l0 = glob.glob(os.path.join(dir0, '*.m4a'))
    return self.load(l0, sort0=sort0)
    
  def __repr__(self):
    """utf-8 formatted text representation"""
    return "; ".join( [str(x) for x in self.data] )
