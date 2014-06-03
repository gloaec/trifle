# -*- coding: utf-8 -*-
import os
from flask import Flask, request, render_template

from trifle.server.views import *

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [
    api,
    frontend,
    monitor,
    configure
]

def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = "Trifle"
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name,
            #instance_path=INSTANCE_FOLDER_PATH, 
	    instance_relative_config=True)

    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    #app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    #app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)

    app.root_path = os.path.abspath(os.path.dirname(__file__))
    app.static_folder = 'static'
    app.templates_folder = 'templates'
    app.secret_key = 'A0Zr98j/3&oaKoaygXfAZsdER~?aijmN]LWX/,?RT'

    # Use instance folder instead of env variables to make deployment easier.
    #app.config.from_envvar('%s_APP_CONFIG' % DefaultConfig.PROJECT.upper(), silent=True)


def configure_hook(app):
    """ Configure the application hooks """
    @app.before_request
    def before_request():
        pass


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

