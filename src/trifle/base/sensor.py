import abc
import os
import logging
from rdflib import BNode, ConjunctiveGraph, plugin, \
                   URIRef, Literal, Namespace, RDF, RDFS
from rdflib.parser import Parser
from rdflib.serializer import Serializer

T = Namespace('http://trifle/#')
logger = logging.getLogger('trifle')

class BaseSensor(object):

    __metaclass__ = abc.ABCMeta
    _base_uri = "http://trifle"
    _path = "/"
    _graph = ConjunctiveGraph()

    def uri(self, path=""):
        return os.path.join(self._base_uri, self._path, path)

    def uri_ref(self, ref, path=""):
        return URIRef(os.path.join(self.uri(path), ref))

    def get_instances_of(self, classname):
        return [s for s in self._graph[:RDF.type/RDFS.subClassOf*'*':
                self.uri_ref(classname)]]

    def get_instances(self):
        return [s for s in self._graph[:RDF.type/RDFS.subClassOf*'*':]]

    def _pull(self, debug=True, verbose=False):
        logger.info("Pulling from %s..."%(self.__class__.__name__))
	self.pull()
	if(debug): 
            instances = self.get_instances()
	    logger.debug("%s informations sensored" % len(instances))
	    if(verbose):
	        for instance in instances:
	            logger.verbose(instance)

    def pull(self):
        raise NotImplementedError('Sensor::pull() needs to be implemented')
        
