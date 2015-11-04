__author__ = 'MBK'

import unittest
from mock import Mock, patch
from app.markov.models import Lyric


class TestLyric(unittest.TestCase):

    def setUp(self):
        self.lyric = Lyric()

if __name__ == '__main__': #pragma: no cover
    unittest.main()
