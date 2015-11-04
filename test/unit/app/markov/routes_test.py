__author__ = 'MBK'

import unittest
from app import create_app


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.app = create_app('development').test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)

if __name__ == '__main__': #pragma: no cover
    unittest.main()
