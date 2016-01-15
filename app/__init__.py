__author__ = 'MBK'

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect
from config import config
from pymongo import MongoClient


client = MongoClient()
db = client['rap_lyricist']


bootstrap = Bootstrap()
csrf = CsrfProtect()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    csrf.init_app(app)

    from .markov import markov as markov_blueprint
    app.register_blueprint(markov_blueprint)

    return app
