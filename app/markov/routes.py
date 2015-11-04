__author__ = 'MBK'

import random
import threading
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import render_template, redirect, url_for, \
    request, current_app, make_response, abort, jsonify
from .models import Lyric
from .loaders import ExampleLoader
from . import markov, tweet
from .. import db
from pprint import pprint


lyrics = db['lyrics']


@markov.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        lyric = request.form.get('lyric')
        upvoted = request.form.getlist('positive')
        lyric_id = ObjectId(request.form.getlist('lyric_id')[0])
        if upvoted:
            example = lyrics.find_one_and_update({'_id': lyric_id}, {'$inc': {'upvotes': 1}})
            t1 = threading.Thread(name='tweet', target=post_tweet, args=(lyric,))
            t2 = threading.Thread(name='process_chains', target=ExampleLoader, args=(example['tokens'],))
            t1.start()
            t2.start()
        else:
            lyrics.find_one_and_update({'_id': lyric_id}, {'$inc': {'downvotes': 1}})
        return redirect(url_for('markov.index'))
    elif request.method == 'GET':

        lyric = Lyric()
        lyric_json = lyric.get_json()
        lyric_id = lyrics.insert(lyric_json)
        lyric_json['_id'] = str(lyric_id)

        return render_template('markov/index.html',
                               lyric=lyric_json,
                               stats=stats())



@markov.errorhandler(Exception)
def page_not_found(e):
    print('caught error', e)
    return render_template('markov/error.html', stats=stats())


# a route for generating sitemap.xml
@markov.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []
    time_diff = datetime.now() - timedelta(days=5)
    age = time_diff.strftime('%Y-%m-%d')
    # static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(
                [rule.rule, age]
            )
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


def post_tweet(lyric):
    dope = ('A1', 'Def', 'Dope', 'Fresh To Death', 'Hella Tight',
            'John Blaze', 'Legit', 'Proper', 'Trump Tight')

    hashtag = ' #' + random.choice(dope).replace(' ', '') + ' #HipHop'
    tweet.post_status(lyric + hashtag)


def stats():
    ups = sorted([result['timestamp'] for result in db.lyrics.find({'author': 'rap_lyricist', 'upvotes': 1})])
    downs = sorted([result['timestamp'] for result in db.lyrics.find({'author': 'rap_lyricist', 'downvotes': 1})])
    num_ups, num_downs = len(ups), len(downs)
    total = num_ups + num_downs
    percentage = round((num_ups / total), 4) * 100
    rounded = int(percentage)
    return {'ups': ups, 'downs': downs, 'total': total, 'rounded': rounded, 'percentage': percentage}


