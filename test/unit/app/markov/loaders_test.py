__author__ = 'MBK'

import unittest
from app.markov.loaders import Loader


class TestLoader(unittest.TestCase):

    def setUp(self):
        self.loader = Loader()




if __name__ == '__main__': #pragma: no cover
    unittest.main()
