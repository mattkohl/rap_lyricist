__author__ = 'MBK'

import threading
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import render_template, current_app, make_response, jsonify
from .models import Lyric, Stats, RLTweet
from .loaders import ExampleLoader
from . import markov, tweet
from .. import db


lyrics = db['lyrics']


@markov.route('/')
def index():
    lyric = create_lyric()

    stats = Stats().get_json()
    return render_template('markov/index.html',
                           lyric=lyric,
                           stats=stats)


@markov.route('/upvote/<lyric_id>', methods=['PUT'])
def upvote_lyric(lyric_id):
    try:
        lyric_id = ObjectId(lyric_id)
    except:
        return make_response(jsonify({'status': 'bad request', 'message': 'invalid value'}), 400)
    else:
        result = lyrics.find_one_and_update({'_id': lyric_id}, {'$inc': {'upvotes': 1}})
        t1 = threading.Thread(name='tweet', target=post_tweet, args=(result['text'],))
        t2 = threading.Thread(name='process_chains', target=ExampleLoader, args=(result['tokens'],))
        t1.start()
        t2.start()
    if result:
        return make_response(jsonify({'status': 'ok'}), 200)
    else:
        return make_response(jsonify({'status': 'not found'}), 404)


@markov.route('/downvote/<lyric_id>', methods=['PUT'])
def downvote_lyric(lyric_id):
    try:
        lyric_id = ObjectId(lyric_id)
    except:
        return make_response(jsonify({'status': 'bad request', 'message': 'invalid value'}), 400)
    else:
        result = lyrics.find_one_and_update({'_id': lyric_id}, {'$inc': {'downvotes': 1}})
    if result:
        return make_response(jsonify({'status': 'ok'}), 200)
    else:
        return make_response(jsonify({'status': 'not found'}), 404)


@markov.route('/getVoteCounts/<lyric_id>')
def get_vote_count(lyric_id):
    lyric_id = ObjectId(lyric_id)
    record = lyrics.find_one({'_id': lyric_id})
    if record:
        upvotes, downvotes = record['upvotes'], record['downvotes']
        return make_response(jsonify({'status': 'ok', 'upvotes': upvotes, 'downvotes': downvotes}), 200)
    else:
        return make_response(jsonify({'status': 'not found'}), 404)


@markov.route('/getNewLyric')
def get_new_lyric():
    return make_response(jsonify(create_lyric()), 200)


@markov.route('/getStats')
def get_stats():
    stats = Stats().get_json()
    return make_response(jsonify(stats), 200)


@markov.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []
    time_diff = datetime.now() - timedelta(days=5)
    age = time_diff.strftime('%Y-%m-%d')
    # static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0 and 'getNewLyric' not in rule.rule and 'getStats' not in rule.rule:
            pages.append(
                [rule.rule, age]
            )
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


def post_tweet(lyric):
    t = RLTweet(lyric)
    tweet.post_status(t.get_text())


def create_lyric():
    lyric = Lyric()
    lyric_dict = lyric.get_json()
    lyric_id = lyrics.insert(lyric_dict)
    lyric_dict['_id'] = str(lyric_id)
    return lyric_dict