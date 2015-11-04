__author__ = 'MBK'

import random
from datetime import datetime
from .. import db


class Lyric:

    pops = ('a', 'an', 'and', 'but', 'for', 'gettin',
            'I', 'if', 'my', 'of', 'or', 'the',
            'they', 'to', 'we', 'when', 'with', )
    starts = ('I', 'He', 'Ma fucka', 'Mothafucka', 'Niggas',
              'She', 'That', 'That shit', 'We', )

    def __init__(self, author='rap_lyricist', chain_size=3):
        self.begins = db['begins']
        self.ends = db['ends']
        self.chains = db['chains']
        self.tokens = []
        self.upvotes = 0
        self.downvotes = 0
        self.timestamp = datetime.utcnow()
        self.author = author
        self.size = 7
        self.chain_size = chain_size
        self.generate_lyric()

    def generate_lyric(self):

        intro = random.choice(list(self.begins.find()))
        self.add_tokens(intro['key'] + [random.choice(intro['following'])])

        for i in range(self.size):
            last_word_length = self.chain_size - 1
            last_words = self.tokens[-1 * last_word_length:]
            key = last_words
            found = self.chains.find_one({'key': key})
            # try second order
            if found:
                candidates = found['following']
                next_word = [random.choice(candidates)]
                self.add_tokens(next_word)
            else:
                key = [last_words[-1]]
                found = self.chains.find_one({'key': key})
                # try first order
                if found:
                    candidates = found['following']
                    next_word = [random.choice(candidates)]
                    self.add_tokens(next_word)
                else:
                    break

        self.finish()
        self.stylize()

    def add_tokens(self, tokens):
        self.tokens.extend(tokens)

    def get_text(self):
        return ' '.join(self.tokens)

    @staticmethod
    def remove_punctuation(tokens):
        return [l.replace(',', '').replace('!', '').replace('?', '').replace('"', '') for l in tokens]

    def finish(self):
        key = self.tokens[-1:]
        key_text = ''.join(key)
        found = self.ends.find_one({'key': key})
        if found:
            choice = [random.choice(found['following'])]
            self.add_tokens(choice)
        elif self.is_punctuated(key_text):
            new_key = self.remove_punctuation(self.tokens[-2:])
            found = self.ends.find_one({'key': new_key})
            if found:
                self.tokens = self.tokens[:-3] + self.remove_punctuation(self.tokens[-2:])
                self.finish()

        self.tail()
        self.start()

    @staticmethod
    def is_punctuated(text):
        return ',' in text or '!' in text or '?' in text or '"' in text

    def tail(self):
        tail = self.tokens[-1]
        if tail in self.pops:
            popped = self.tokens.pop()
        ct = 0
        for token in self.tokens:
            ct += token.count('"')
        if ct % 2 != 0:
            tail = self.tokens.pop()
            if tail.count('"') > 0:
                tail = tail.replace('"', '')
            else:
                tail += '"'
            self.add_tokens([tail])

    def start(self):
        if self.tokens[0].endswith('ed'):
            start = random.choice(self.starts)
            self.tokens = [start] + self.tokens

    def stylize(self):
        start = self.tokens[0]
        if start == start.lower():
            self.tokens = [start.title()] + self.tokens[1:]

        finished = self.tokens
        finished[-1] = finished[-1].rstrip(',')
        for i in range(len(finished)):
            token = finished[i]
            if i > 0 and token[0].isupper():
                if finished[i-1].endswith('?'):
                    finished[i] = token[0].upper() + token[1:]
                elif self.count_following([token]) > self.count_following([token.lower()]):
                    pass
                else:
                    finished[i] = token.lower()
        self.tokens = finished

    def count_following(self, key):
        result = self.chains.find_one({'key': key})
        if result:
            return len(result['following'])
        else:
            return 0

    def jsonify(self):
        d = {
            'author': self.author,
            'tokens': self.tokens,
            'text': self.get_text(),
            'timestamp': self.timestamp,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes
        }
        return d
