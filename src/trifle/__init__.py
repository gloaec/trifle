# -*- coding: utf-8 -*-
from flask import Flask

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['ini', 'eol'])

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

from trifle import ontology
from trifle import agents

