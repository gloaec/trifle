import logging
from pyparsing import ParseException
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from trifle.store import Store

logger = logging.getLogger('trifle')
monitor = Blueprint('monitor', __name__, url_prefix='/monitor')

@monitor.route('/services', methods=['GET'])
def monitor_services():
    store = Store()
    results = store.graph.query(
        """ SELECT ?ServiceName ?Status
            WHERE { ?Service a :Service . 
                    ?Service :name ?ServiceName .
                    ?Service :status ?Status }""")
    return render_template('monitor/services.html', results=results)

@monitor.route('/ontology', methods=['GET','POST'])
def monitor_ontology():
    store = Store()
    default_query = """ SELECT ?Subject ?Object 
                        WHERE { ?Subject rdfs:subClassOf ?Object }"""
    try:
        results = store.graph.query(request.form.get('query', default_query))
    except ParseException, e:
        results = []
        flash(e.msg, 'danger')
    return render_template('monitor/ontology.html', results=results)
