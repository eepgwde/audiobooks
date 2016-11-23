## @file Test.py
# @author weaves
# @brief Unittest of MInfo
#
# This module tests the ancillary operations and the 
# 
# @note
#
# Relatively complete test.

import minfo 

import sys, logging, os
from unidecode import unidecode

from datetime import datetime, timezone, timedelta, date

from collections import Counter

from MediaInfoDLL3 import MediaInfo

import unittest

from audiobooks.app import Track

logfile = os.environ['X_LOGFILE'] if os.environ.get('X_LOGFILE') is not None else media
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger('Test')
sh = logging.StreamHandler()
logger.addHandler(sh)

media0 = os.path.join(os.path.dirname(__file__), "media")

## A test driver for GMus0
#
# @see GMus0
class Test(unittest.TestCase):
    """
    Test MInfo
    """
    test0 = None
    gmus0 = None
    nums = [-1, 0, 1, 2, 3]
    dir0 = None
    files = []
    logger = None
    
    ## Sets pandas options and logging.
    @classmethod
    def setUpClass(cls):
        global logger
        cls.logger = logger
        
        cls.dir0 = os.environ['SDIR'] if os.environ.get('SDIR') is not None else media0
        
        for root, dirs, files in os.walk(cls.dir0, topdown=True):
            for name in files:
                cls.files.append(os.path.join(root, name))

        cls.files.sort()
        cls.logger.info('files: ' + unidecode('; '.join(cls.files)))
    
    ## Logs out.
    @classmethod
    def tearDownClass(cls):
        pass

    ## Null setup. Create a new one.
    def setUp(self):
        self.logger.info('setup')
        self.file0, *type(self).files = type(self).files
        self.test0 = Track(self.file0)
        return

    ## Null setup.
    def tearDown(self):
        self.logger.info('tearDown')
        return

    ## Loaded?
    ## Is utf-8 available as a filesystemencoding()
    def test_000(self):
        self.assertIsNotNone(self.test0)
        return

    def test_003(self):
        self.logger.info("encoding: " + sys.getfilesystemencoding())
        with self.assertRaises(UnicodeEncodeError):
            filename = 'filename\u4500abc'
            with open(filename, 'w') as f:
                f.write('blah\n')

        self.logger.info('No UTF-8')

    def test_01(self):
        self.assertIsNotNone(self.test0)
        self.logger.info("track: type: " + type(self.test0).__name__)
        self.logger.info('duration: type: ' + type(self.test0.duration).__name__)
        self.logger.info('duration: ' + str(self.test0.duration))
        self.logger.info('duration: ' + str(self.test0.disc_track))

    def test_02(self):
        self.logger.info(': ' + type(yday))

    
    def test_03(self):
        self.logger.info('test_03')
        self.assertIsNotNone(self.test0)
        self.test0.open(self.file0)
        str0 = self.test0.quality()
        self.logger.info('str0:' + self.file0 + "; " + str0)

        format0 = "%H:%M:%S.%f"
        d = datetime.strptime(str0, format0)
        self.logger.info('strptime:' + d.strftime(format0))

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
        unittest.main(module='Test', verbosity=3, failfast=True, exit=False)
