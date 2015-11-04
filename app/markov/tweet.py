__author__ = 'MBK'

import twitter
import os

OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')



def post_status(status):

    auth = twitter.oauth.OAuth(OAUTH_TOKEN,
                               OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY,
                               CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)

    twitter_api.statuses.update(status=status)

if __name__ == '__main__':
    post_status('testing status update')
