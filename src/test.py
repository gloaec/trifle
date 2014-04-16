# -*- coding: utf-8 -*-
import re
import subprocess
from termcolor import colored
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF
from trifle.recipes import getHostname, getServices

VERBOSE   = False
ONTOLOGY  = "/home/ghis/Workspace/trifle/src/ontology.owl"
OUT       = "/home/ghis/Workspace/trifle/src/config.n3"
NAMESPACE = "http://www.semanticweb.org/ontologies/2014/3/trifle#"

g = Graph().parse(ONTOLOGY)
n = Namespace(NAMESPACE)

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
    for service in getServices():
        node    = BNode(service['name'])
        g.add( (node, RDF.type,   n.Service) )
        g.add( (node, n.name,     Literal(service['name'])) )
        g.add( (node, n.status,   Literal(service['status'])) )
        #g.add( (node, RDF.nodeID, BNode(name)) )
        #g.remove( (n., None, None) ) 
    g.serialize(OUT, format='n3')

for service in provided(refresh=True):
    print "Service '%s' on machine '%s' (host: %s | port: %s)" % service
