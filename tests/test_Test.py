## @file Test.py
# @author weaves
# @brief Unittest
#
# @note
#
# Relatively complete test.

import sys, logging, os
from unidecode import unidecode

from datetime import datetime, timezone, timedelta, date

from collections import Counter

import unittest

from audiobooks import Track, Tracks, Book

logfile = os.environ['X_LOGFILE'] if os.environ.get('X_LOGFILE') is not None else "test.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger('Test')
sh = logging.StreamHandler()
logger.addHandler(sh)

media0 = os.path.join(os.path.dirname(__file__), "media")
trs0 = os.path.join(os.path.dirname(__file__), "p1.lst")

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
        self.logger.info('test0: ' + str(self.test0))
        
        self.file0, *type(self).files = type(self).files
        test1 = Track(self.file0)
        self.logger.info('test1: ' + str(test1))
        self.logger.info('test1: duration: ' + str(test1.duration))
        self.logger.info('test1: duration1: ' + str(test1.duration1))
        self.logger.info('test1: filename: ' + str(test1.filename))

    def test_02(self):
        self.logger.info('test_02')
        self.assertIsNotNone(self.test0)
        trs = Tracks(type(self).files)
        self.logger.info('trs: ' + str(trs))
    
    def test_03(self):
        trs = Tracks(type(self).files)
        for tr in trs:
            self.logger.info('tr: ' + str(tr))

    def test_12(self):
        self.logger.info('test_02')
        self.assertIsNotNone(self.test0)
        trs = Tracks(type(self).dir0)
        self.logger.info('trs: ' + str(trs))
    
    def test_15(self):
        trs = Tracks(type(self).dir0)
        for tr in trs:
            self.logger.info('tr: ' + str(tr))

    def test_17(self):
        """
        Load from a file that lists tracks from two discs, but both discs 
        are unnumbered (and therefore disc 1.)
        Don't sort these, use the file order.
        """
        files = []
        with open(trs0, encoding="utf-8") as f:
            files = f.read().splitlines()

        trs = Tracks(files, sort0=False)
        for tr in trs:
            self.logger.info('tr: ' + str(tr))

    def test_19(self):
        """
        As the earlier test, but demonstrate that the sorting works.
        """
        files = []
        with open(trs0, encoding="utf-8") as f:
            files = f.read().splitlines()

        trs = Tracks(files, sort0=True)
        for tr in trs:
            self.logger.info('tr: ' + str(tr))

    def test_21(self):
        """
        Time functions
        """
        files = []
        with open(trs0, encoding="utf-8") as f:
            files = f.read().splitlines()

        trs = Tracks(files, sort0=True)
        for tr in trs:
            self.logger.info('tr: duration: ' + str(tr.duration))
            self.logger.info('tr: duration1: ' + str(tr.duration1))
            self.logger.info('tr: quality0: ' + str(tr.quality0))

    def test_30(self):
        files = []
        with open(trs0, encoding="utf-8") as f:
            files = f.read().splitlines()

        d0 = dict([['sort', True], ['input', files], ['files', []]])
        book = Book(**d0)
        self.logger.info("book: " + str(book))
        self.logger.info("book[0]: album: " + str(book[0].album))
        chapters = book.chapters0()
        self.logger.info("chapters: " + str(len(chapters)))
        self.logger.info("book: " + '\n'.join(chapters))

    def test_43(self):
        logger.info("test_43")
        d0 = dict([['sort', True]])
        d0['files'] = []
        d0['input'] = [ type(self).dir0 ]
        book = Book(**d0)
        file1 = sys.stdout
        file1.writelines(book.chapters0())

    def test_45(self):
        files = []
        with open(trs0, encoding="utf-8") as f:
            files = f.read().splitlines()
        d0 = dict([['sort', False]])
        d0['files'] = trs0
        d0['input'] = []
        d0['cover'] = "abc.jpg"
        d0['output0'] = "abc.m4b"
        book = Book(**d0)

    def test_47(self):
        files = []
        with open(trs0, encoding="utf-8") as f:
            files = f.read().splitlines()
        d0 = dict([['sort', False]])
        d0['files'] = trs0
        d0['input'] = []
        d0['dry-run'] = True
        d0['cover'] = "abc.jpg"
        d0['output0'] = "abc.m4b"
        book = Book(**d0)
        book.write()

    def test_49(self):
        files = []
        with open(trs0, encoding="utf-8") as f:
            files = f.read().splitlines()
        d0 = dict([['sort', False]])
        d0['files'] = trs0
        d0['input'] = []
        d0['dry-run'] = True
        d0['cover'] = "abc.jpg"
        d0['output0'] = "abc.m4b"
        book = Book(**d0)
        book.chapters0()
        book.chapters()

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

