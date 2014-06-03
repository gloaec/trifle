import logging
from pyparsing import ParseException
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from trifle.store import Store

logger = logging.getLogger('trifle')
configure = Blueprint('configure', __name__, url_prefix='/configure')

@configure.route('/<serverid>', methods=['GET'])
def configure_server(serverid):
    return render_template('configure/server.html', serverid=serverid)
