import logging

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from trifle.store import Store

logger = logging.getLogger('trifle')
monitor = Blueprint('monitor', __name__, url_prefix='/monitor')

@monitor.route('/ontology', methods=['GET'])
def get_ontology():
    store = Store()
    results = store.graph.query(
        """ SELECT ?subject ?object 
            WHERE { ?subject rdfs:subClassOf ?object }""")
    return render_template('monitor/ontology.html', results=results)

@monitor.route('/ontology', methods=['POST'])
def query_ontology():
    store = Store()
    results = store.graph.query(request.form.get('query',''))
    return render_template('monitor/ontology.html', results=results)
