import abc
import os
import logging; logger = logging.getLogger('trifle')
from rdflib import ConjunctiveGraph, URIRef, Literal

from trifle import config
from trifle.namespaces import RDF, RDFS, T, DC, FOAF, IMDB, REV

class BaseSensor(object):

    __metaclass__ = abc.ABCMeta
    path          = "/"
    queries       = {}

    def __init__(self, 
            graph        = None,
	    path         = None,
            storefile    = None,
            storeuri     = config['STORE_URI'], 
            namespaces   = config['NAMESPACES'],
            format       = config['FORMAT']):

        if graph is not None: 
            self.graph      = graph
        else: 
            self.graph      = ConjunctiveGraph()
        if path is not None: 
            self.path       = path
        if storefile is not None: 
            self.storefile  = storefile
        else:
            self.storefile  = os.path.join(config['STORE_DIR'],
                              '%s.%s'%(self.__class__.__name__, format))
        self.storeuri       = storeuri
        self.namespaces     = namespaces
        self.format         = format

        for namespace, uri in namespaces.iteritems():
            self.namespaces[namespace] = uri
        #if os.path.exists(storefile):
        #    self.graph.load(storeuri, format=format)
        for namespace, uri in self.namespaces.iteritems():
            self.graph.bind(namespace, uri)

    def uri(self, path=""):
        return os.path.join(self.storeuri, self.path, path)

    def uri_ref(self, ref, path=""):
        return URIRef(os.path.join(self.uri(path), ref))

    def get_instances_of(self, classname):
        return [s for s in self.graph[:RDF.type/RDFS.subClassOf*'*':
                self.uri_ref(classname)]]

    def get_instances(self):
        return [s for s in self.graph[:RDF.type/RDFS.subClassOf*'*':]]

    def snapshot(self, debug=True, verbose=False, serialize=True):
        logger.info("Pulling from %s..."%(self.__class__.__name__))
	self.pull()
	if(serialize): 
            self.graph.serialize(self.storefile, format='n3')
	if(debug): 
            instances = self.get_instances()
	    logger.debug("%s informations sensored" % len(instances))
	    if(verbose):
	        for instance in instances:
	            logger.verbose(instance)
        return self.graph

    def pull(self):
        raise NotImplementedError('Sensor::pull() needs to be implemented')
