__author__ = 'MBK'

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from config import config
from pymongo import MongoClient


client = MongoClient()
db = client['rap_lyricist']


bootstrap = Bootstrap()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)

    from .markov import markov as markov_blueprint
    app.register_blueprint(markov_blueprint)

    return app
