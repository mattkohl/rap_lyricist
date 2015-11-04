__author__ = 'MBK'

import sys
import logging
import os

cwd = os.getcwd()
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.join(cwd, 'app'))

from manage import app
app.run()
