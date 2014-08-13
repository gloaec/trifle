# -*- coding: utf-8 -*-
import datetime
import os
import sys
import re
import time
from rdflib import BNode, ConjunctiveGraph, plugin, URIRef, Literal, Namespace
from rdflib.parser import Parser
from rdflib.serializer import Serializer

from trifle.namespaces import *
from trifle.sensors import *
from trifle import config

r_who = re.compile('^(.*?) <([a-z0-9_-]+(\.[a-z0-9_-]+)*@[a-z0-9_-]+(\.[a-z0-9_-]+)+)>$')

plugin.register("rdfjson", Parser,
    "rdflib.plugins.parsers.rdfjson", "JsonParser")
plugin.register("rdfjson", Serializer,
    "rdflib.plugins.serializers.rdfjson", "JsonSerializer")

class Store:

    def __init__(self, 
            storefile  = config['STORE_FILE'],
            storeuri   = config['STORE_URI'], 
            structfile = config['STRUCT_FILE'],
            structuri  = config['STRUCT_URI'],
            namespaces = config['NAMESPACES'],
            sensors    = config['SENSORS'],
            format     = config['FORMAT']):

        self.storeuri   = storeuri
        self.storefile  = storefile
        self.structuri  = structuri
        self.structfile = structfile
        self.namespaces = namespaces
        self.sensors    = sensors
        self.format     = format

        for namespace, uri in namespaces.iteritems():
            self.namespaces[namespace] = uri

        self.reset()

    def reset(self, new_graph=None):
        if new_graph is not None:
            self.graph = new_graph	
        else:
            self.graph = ConjunctiveGraph()
        for namespace, uri in self.namespaces.iteritems():
            self.graph.bind(namespace, uri)
        if os.path.exists(self.structfile):
            self.graph.load(self.structuri, format=self.format)
        if os.path.exists(self.storefile):
            self.graph.load(self.storeuri, format=self.format)

    def save(self, format=None):
        if not format: format = self.format
        self.graph.serialize(self.storeuri, format=format)

    def get(self, something): 
        pass

    def snapshot(self):
        self.reset()
        for sensor in self.sensors:
            constructor = globals()[sensor]
            instance = constructor()
            instance.snapshot()
            self.graph = self.graph + instance.graph

    @property
    def queries(self):
        q = self.basequeries
        for sensor in self.sensors:
            constructor = globals()[sensor]
            q = dict(q, **constructor.queries)
        return q

    @property
    def local(self):
        """ Idee: local config only """
        hostname = getHostname()
        query = "?m a :Machine . ?m location %s" % hostname
        return hostname

    def on(self, ip=None):
        """ Idee: store.on('192.168.1.43').query('SELECT..') """

    def query(self, sparql):
        return self.graph.query(sparql)

    def register(self):
        name = getHostname()
        location = ""



    def who(self, who=None):
        if who is not None:
            name, email = (r_who.match(who).group(1), r_who.match(who).group(2))
            self.graph.add((URIRef(storeuri), DC['title'], Literal(title % name)))
            self.graph.add((URIRef(storeuri+'#author'), RDF.type, FOAF['Person']))
            self.graph.add((URIRef(storeuri+'#author'), FOAF['name'], Literal(name)))
            self.graph.add((URIRef(storeuri+'#author'), FOAF['mbox'], Literal(email)))
            self.save()
        else:
            return self.graph.objects(URIRef(storeuri+'#author'), FOAF['name'])

    def new_movie(self, movie):
        movieuri = URIRef('http://www.imdb.com/title/tt%s/' % movie.movieID)
        self.graph.add((movieuri, RDF.type, IMDB['Movie']))
        self.graph.add((movieuri, DC['title'], Literal(movie['title'])))
        self.graph.add((movieuri, IMDB['year'], Literal(int(movie['year']))))
        self.save()

    def new_review(self, movie, date, rating, comment=None):
        review = BNode() # @@ humanize the identifier (something like #rev-$date)
        movieuri = URIRef('http://www.imdb.com/title/tt%s/' % movie.movieID)
        self.graph.add((movieuri, REV['hasReview'], URIRef('%s#%s' % (storeuri, review))))
        self.graph.add((review, RDF.type, REV['Review']))
        self.graph.add((review, DC['date'], Literal(date)))
        self.graph.add((review, REV['maxRating'], Literal(5)))
        self.graph.add((review, REV['minRating'], Literal(0)))
        self.graph.add((review, REV['reviewer'], URIRef(storeuri+'#author')))
        self.graph.add((review, REV['rating'], Literal(rating)))
        print comment
        if comment is not None:
            self.graph.add((review, REV['text'], Literal(comment)))
        self.save()

    def movie_is_in(self, uri):
        return (URIRef(uri), RDF.type, IMDB['Movie']) in self.graph

    basequeries = {
        "Trifle Entities": """
            SELECT ?Subject ?Object 
            WHERE { ?Subject rdfs:subClassOf ?Object }
        """
    }

def help():
    print __doc__.split('--')[1]

def main(argv=None):
    if not argv:
        argv = sys.argv
    s = Store()
    if argv[1] in ('help', '--help', 'h', '-h'):
        help()
    elif argv[1] == 'whoami':
        if os.path.exists(storefile):
            print list(s.who())[0]
        else:
            s.who(argv[2])
    elif argv[1].startswith('http://www.imdb.com/title/tt'):
        if s.movie_is_in(argv[1]):
            raise
        else:
            i = imdb.IMDb()
            movie = i.get_movie(argv[1][len('http://www.imdb.com/title/tt'):-1])
            print '%s (%s)' % (movie['title'].encode('utf-8'), movie['year'].encode('utf-8'))
            for director in movie['director']:
                print 'directed by: %s' % director['name'].encode('utf-8')
            for writer in movie['writer']:
                print 'writed by: %s' % writer['name'].encode('utf-8')
            s.new_movie(movie)
            rating = None
            while not rating or (rating > 5 or rating <= 0):
                try:
                    rating = int(raw_input('Rating (on five): '))
                except ValueError:
                    rating = None
            date = None
            while not date:
                try:
                    i = raw_input('Review date (YYYY-MM-DD): ')
                    date = datetime.datetime(*time.strptime(i, '%Y-%m-%d')[:6])
                except:
                    date = None
            comment = raw_input('Comment: ')
            s.new_review(movie, date, rating, comment)
    else:
        help()

if __name__ == '__main__':
    main()
