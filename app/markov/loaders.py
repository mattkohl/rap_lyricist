__author__ = 'MBK'

import os
import json
from datetime import datetime
from config import APP_STATIC
from .. import db

begin_chains = db['begins']
end_chains = db['ends']
chains = db['chains']
lyrics = db['lyrics']


class Loader:

    def __init__(self, order=1):
        self.order = order
        self.chain_size = self.order + 1
        self.begins = begin_chains
        self.ends = end_chains
        self.cache = chains

    def words_at_position(self, line, i):
        chain = []
        for chain_index in range(0, self.chain_size):
            chain.append(line[i + chain_index])
        return chain

    def line_chains(self, line):
        size = len(line)
        extent = size - self.order
        if size < self.chain_size:
            return
        for i in range(extent):
            chain = tuple(self.words_at_position(line, i))
            if i == 0:
                self.capture_chain(chain, begin_chains)
            if i == extent - 1:
                self.capture_chain(chain, end_chains)
            self.capture_chain(chain, chains)

    def capture_chain(self, chain, collection):
        if len(chain) > self.order:
            key = chain[0:self.order]
            following = [chain[self.order]]
            found = collection.find_one({'key': key})
            if found:
                tmp = found['following']
                tmp.extend(following)
                collection.find_one_and_update({'key': key}, {'$set': {'following': tmp}})
            else:
                collection.insert_one({'key': key, 'following': following})

class ExampleLoader(Loader):

    def __init__(self, line):
        Loader.__init__(self)
        self.line_chains(line)
        print("Processed:", line)


class JsonLoader(Loader):

    def __init__(self, source_json):
        """
        source_json schema:

        {
            'lyrics': [
                {
                    'tokens': ['a', 'b', 'c'],
                    'author': 'xyz'
                }
            ]
        }

        """
        Loader.__init__(self)
        self.source = source_json
        self.data = self.read_source()
        self.process_lines()

    def read_source(self):
        with open(self.source) as f:
            data = json.load(f)
        print('Successfully loaded', self.source)
        if 'lyrics' in data:
            return data
        else:
            return {}

    def process_lines(self):
        print(len(self.data['lyrics']), "objects to process.")
        print("Let's do this.")
        index = 0
        for lyric in self.data['lyrics']:
            if index % 1000 == 0:
                print('Processed', index, 'objects...')
            index += 1
            tokens = lyric['tokens']
            found = lyrics.find_one({'tokens': tokens})
            if found:
                continue  # print('Already in db:', tokens)
            else:
                update = {
                    'text': ' '.join(tokens),
                    'timestamp': datetime.utcnow(),
                    'upvotes': 0,
                    'downvotes': 0
                }
                lyric.update(update)
                lyric_id = lyrics.insert(lyric)
                self.line_chains(tokens)
                print("Processed:", lyric_id, "--", tokens)
                break


if __name__ == "__main__":
    source = os.path.join(APP_STATIC, 'text', 'lyrics.json')
    JsonLoader(source)
