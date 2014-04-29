from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from trifle.store import Store

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/config', methods=['GET'])
def get_config():
    store      = Store()
    return store.graph.serialize(None, format='rdfjson')
    #return jsonify(store_dict)
