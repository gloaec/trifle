# -*- coding: utf-8 -*-
from os.path import dirname, join, realpath
from trifle.namespaces import RDF, RDFS, T, DC, FOAF, IMDB, REV

root_dir = dirname(realpath(__file__))

config = {
    'ROOT_DIR'   : root_dir,
    'STORE_DIR'  : join(root_dir, 'store'),
    'STORE_FILE' : join(root_dir, 'store.n3'),
    'STRUCT_FILE': join(root_dir, 'structure.n3'),
    'STORE_URI'  : 'file://%s'%join(root_dir, 'store.n3'),
    'STRUCT_URI' : 'file://%s'%join(root_dir, 'structure.n3'),
    'NAMESPACES' : {
	'rdf' : RDF,
	'rdfs': RDFS,
        't'   : T,
        'dc'  : DC,
        'foaf': FOAF,
        'imdb': IMDB,
        'rev' : REV
    },
    'SENSORS' : [
        'InterfacesSensor',
        'ProcessesSensor',
        'UsersSensor'
    ],
    'FORMAT' : 'n3'
}
