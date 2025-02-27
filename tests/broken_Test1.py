## @file Test1.py
# @author weaves
# @brief Unittest of MInfo
#
# This module tests the ancillary operations and the 
# 
# @note
#
# Relatively complete test.

import sys, logging, os
from unidecode import unidecode

from datetime import datetime, timezone, timedelta, date
from audiobooks import Track, Tracks, Book, MInfo, MInfo1

from collections import Counter

from MediaInfoDLL3 import MediaInfo

import unittest

## Audiobook compiler
#

logfile = os.environ['X_LOGFILE'] if os.environ.get('X_LOGFILE') is not None else "test.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger('Test')
sh = logging.StreamHandler()
logger.addHandler(sh)

media0 = os.path.join(os.path.dirname(__file__), "media")
trs0 = os.path.join(os.path.dirname(__file__), "p1.lst")


class Test1(unittest.TestCase):
    """
    Test MInfo1
    """

    flag0=False
    test0 = None
    dir0 = None
    files0 = []
    files = []
    logger = None


    @classmethod
    def setUpClass(cls):
        cls.logger = logger
        cls.dir0 = os.environ['SDIR'] if os.environ.get('SDIR') is not None else media0
        
        for root, dirs, files in os.walk(cls.dir0, topdown=True):
            for name in files:
                cls.files.append(os.path.join(root, name))

        cls.files.sort()
        cls.files0 = cls.files
        cls.logger.info('files: ' + unidecode('; '.join(cls.files)))


    ## Null setup. Create a new one.
    def setUp(self):
        self.logger.info('setup')
        if not self.flag0:
            self.setUpClass()
            self.flag0 = True
        self.file0, *type(self).files = type(self).files
        self.test0 = self.file0
        return

    ## Null setup.
    def tearDown(self):
        self.logger.info('tearDown')
        return

    ## Loaded?
    ## Is utf-8 available as a filesystemencoding()
    def test_000(self):
        import pdb; pdb.set_trace()
        x0 = Track(self.test0)
        self.assertIsNotNone(self.test0)
        self.test0.open(self.file0)
        return

    def test_05(self):
        self.assertIsNotNone(self.test0)
        minfo = self.test0
        d = minfo.duration()
        self.logger.info("duration: " + d.isoformat())
        return

    def test_10(self):
        self.files = []
        for root, dirs, files in os.walk(self.dir0, topdown=True):
            for name in files:
                self.files.append(os.path.join(root, name))

        self.files.sort()
        self.file0, *self.files = self.files
        minfo = MInfo1(l0 = self.file0, delegate0 = "duration2")
        minfo.set_delegate("duration2")

        for f in self.files:
            self.logger.info("load: " + f)
            x0 = minfo.next(f)
            logging.info("duration: cum: " + type(x0).__name__ +
                         "; " + "; ".join(x0))

#
# The sys.argv line will complain to you if you run it with ipython
# emacs. The ipython arguments are passed to unittest.main.

if __name__ == '__main__':
    if len(sys.argv) and "ipython" not in sys.argv[0]:
        # If this is not ipython, run as usual
        unittest.main(sys.argv)
    else:
        # If not remove the command-line arguments.
        sys.argv = [sys.argv[0]]
        unittest.main(module='Test1', verbosity=3, failfast=True, exit=False)
