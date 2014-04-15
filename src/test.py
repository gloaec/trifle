# -*- coding: utf-8 -*-
import re
import subprocess
from termcolor import colored
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF

g = Graph().parse("/home/ghis/Workspace/trifle/src/ontology.owl")
n = Namespace("http://www.semanticweb.org/ontologies/2014/3/trifle#")

def provided(refresh=False):
    """ List of services available in the environemment """
    if refresh: pull()
    return g.query(
        """ SELECT ?service ?machine ?host ?port 
            WHERE {
                ?service a :Service .
                ?service :providedBy  ?machine .
                ?machine :location    ?host .
                ?service :servicePort ?port .
            }""")


def pull(): 
    cmd = 'service --status-all 2>&1'
    exc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in exc.stdout:
         info = re.search('\[\s?([+-\??])\s?\]\s+(.*)', line, re.IGNORECASE)
         if info:
            status  = {'+': True, '-': False, '?': None}[info.group(1)]
            pstatus = {'+': 'on', '-': 'off', '?': 'unknown'}[info.group(1)]
            pcolor  = {'+': 'green', '-': 'red', '?': 'grey'}[info.group(1)]
            name    = info.group(2).strip()
            node    = BNode(name)
            g.add( (node, RDF.type,   n.Service) )
            g.add( (node, n.name,     Literal(name)) )
            g.add( (node, n.status,   Literal(status)) )
            #g.add( (node, RDF.nodeID, BNode(name)) )
            #g.remove( (n., None, None) ) 
            print "%40s" % name, colored(pstatus, pcolor, attrs=['bold'])
    print g.serialize(format='turtle')

for service in provided(refresh=True):
    print "Service '%s' on machine '%s' (host: %s | port: %s)" % service


