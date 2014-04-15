# -*- coding: utf-8 -*-
import rdflib

g = rdflib.Graph()
g.parse("/home/ghis/Workspace/trifle/src/ontology.owl")

def provided():
    """ List of services available in the environemment """
    return g.query(
        """ SELECT ?service ?machine ?host ?port 
            WHERE {
                ?service a :Service .
                ?service :providedBy  ?machine .
                ?machine :location    ?host .
                ?service :servicePort ?port .
            }""")

for service in provided():
    print "Service '%s' on machine '%s' (host: %s | port: %s)" % service


