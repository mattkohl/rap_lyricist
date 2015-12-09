__author__ = 'MBK'

import unittest
import mongomock

from datetime import datetime
from mock import MagicMock
from app.markov.models import Lyric, Stats, db


class TestStats(unittest.TestCase):

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

    def setUp(self):
        self.json = {
            'upCount': 3,
            'downCount': 4
        }



class TestLyric(unittest.TestCase):

    def setUp(self):
        self.lyric = MagicMock()

if __name__ == '__main__': #pragma: no cover
    unittest.main()
