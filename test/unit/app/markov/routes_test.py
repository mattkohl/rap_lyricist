__author__ = 'MBK'

import unittest
from mock import patch, MagicMock
from app import create_app
from app.markov.routes import index, get_stats


class TestGetStats(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing').test_client()


if __name__ == '__main__': #pragma: no cover
    unittest.main()
