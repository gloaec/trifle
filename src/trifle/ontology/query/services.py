# -*- coding: utf-8 -*-
import rdflib

g = rdflib.Graph()
g.parse("/home/ghis/Workspace/trifle/src/ontology.owl")

def providedLocally(machine=None):
    return g.query(
        """ SELECT DISTINCT ?aname ?bname
            WHERE {
              ?a foaf:knows ?b .
              ?a foaf:name ?aname .
              ?b foaf:name ?bname .
            }""")


def provided():
    """ List of services available in the environemment """
    return g.query(
        """ SELECT ?service ?machine ?host ?port 
            WHERE {
                ?service rdf:type :Service .
                ?service :providedBy ?whatever .
                ?service :serviceHost ?host .
                ?service :servicePort ?port .
            }""")

