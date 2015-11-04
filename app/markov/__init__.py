__author__ = 'MBK'

from flask import Blueprint

markov = Blueprint('markov', __name__)

from . import routes