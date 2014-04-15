# -*- coding: utf-8 -*-
from trifle.ontology import g

def providedLocally(machine=None):
    return g.query(
        """ SELECT DISTINCT ?aname ?bname
            WHERE {
              ?a foaf:knows ?b .
              ?a foaf:name ?aname .
              ?b foaf:name ?bname .
            }""")


def provided():
    return g.query(
        """ SELECT ?service ?machine ?host ?port 
            WHERE {
                ?service rdf:type :Service .
                ?service :providedBy ?whatever .
                ?service :serviceHost ?host .
                ?service :servicePort ?port .
            }""")

