# -*- coding: utf-8 -*-
import os
import inspect
import glob
import types

from flask import Flask, url_for, json, jsonify, g, request, Response, \
                  render_template, make_response, send_from_directory
from jinja2 import Environment, FileSystemLoader
# --------------------

def basedir():
    cwd = os.getcwd()
    directories = cwd.split(os.sep)
    for index, directory in reversed(list(enumerate(directories))):
        path = os.path.join('/', *directories[:index+1])
        if os.path.exists(os.path.join(path, 'setup.py')):
            return path
    return None


def appdir():
    _basedir = basedir() 
    if _basedir is None: return None
    _basename = os.path.basename(_basedir)
    _appdir = os.path.join(_basedir, _basename)
    if os.path.exists(_appdir): 
	return _appdir
    for directory in os.walk(_basedir).next()[1]:
        path = os.path.join(_basedir, directory)
        if os.path.exists(os.path.join(path, 'config', '__init__.py')):
            return path
    return None


def get_submodules(module_name):
    modules = []
    try:
        module = __import__(module_name, globals(), locals(), [module_name.split('.')[-1]])
    except ImportError:
        return modules
    for name in dir(module):
        if type(getattr(module, name)) == types.ModuleType:
            submodule = '.'.join([module_name, name])
            modules.append(__import__(submodule, globals(), locals(), [submodule.split('.')[-1]]))
    return modules


def find_subclasses(module):
    return list(set([
        cls
            for name, cls in inspect.getmembers(module)
                if inspect.isclass(cls)
    ]))

	    
def import_mod(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def import_all_models(path):
    for f in glob.glob(os.path.join(os.path.dirname(path),"*.py")):
        model = os.path.basename(f)[:-3] 
        if model != '__init__':
            mod_name = 'app.models.%s' % model
            try:
                mod = __import__(model, globals(), locals(), fromlist=[model.title()])
                klass = getattr(mod, model.title())
                if not '%s' % model.title() in locals(): 
                    locals()[model.title()] = klass
            except ImportError:
                print 'Failed to import Model: ', model


def generate_template(src, dest, **kwargs):
    _basedir = basedir()
    _pkgdir = os.path.abspath(os.path.dirname(__file__))

    print "Generating %s" % dest

    env = Environment(loader=FileSystemLoader(os.path.join(_pkgdir, 'templates')))
    template = env.get_template(src)
    output_from_parsed_template = template.render(**kwargs)
    with open(os.path.join(_basedir, dest), "wb") as fh:
        fh.write(output_from_parsed_template.encode('utf-8'))


def generate_directory(directory):
    _basedir = basedir()
    path = os.path.join(_basedir, directory)
    if not os.path.exists(path):
        print "Creating directory %s" % directory
        os.makedirs(path)


def append_in_file(src, append_string):
    _basedir = basedir()
    path = os.path.join(_basedir, src)
    with open(path, "a") as fh:
        fh.write(append_string)


def json_response(body, status_code=200):
    resp = make_response(json.dumps(body))
    resp.status_code = status_code
    resp.mimetype = 'application/json'
    return resp


def error_response(msg, status_code=500, to_json=False):
    if(to_json): msg = json.dumps(msg)
    resp = make_response(msg)
    resp.status_code = status_code
    resp.mimetype = ('application/json','text/plain')[to_json]
    return resp


def bad_id_response(id):
        return error_response("Invalid id: %s" % id, 400)



