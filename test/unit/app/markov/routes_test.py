__author__ = 'MBK'

import unittest
import mongomock
from datetime import datetime
from app import create_app


class TestStats(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing').test_client()
        lyrics = mongomock.MongoClient().db.collection
        objects = [
            {'author': 'rap_lyricist', 'upvotes': 1},
            {'author': 'rap_lyricist', 'upvotes': 1},
            {'author': 'rap_lyricist', 'upvotes': 1},
            {'author': 'rap_lyricist', 'downvotes': 1},
            {'author': 'rap_lyricist', 'downvotes': 1},
            {'author': 'rap_lyricist', 'downvotes': 1},
            {'author': 'rap_lyricist', 'downvotes': 1}
        ]
        for obj in objects:
            obj['timestamp'] = datetime.utcnow()
            obj['_id'] = lyrics.insert(obj)


if __name__ == '__main__': #pragma: no cover
    unittest.main()
