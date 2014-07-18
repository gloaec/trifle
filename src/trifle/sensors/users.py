# -*- coding: utf-8 -*-
import os
import psutil

from trifle.base.sensor import BaseSensor, RDF, T, Literal

URI = "file:///home/ghis/Workspace/trifle/src/trifle/ontologies/users.n3"

class UsersSensor(BaseSensor):

    def pull(self):
        for user in psutil.users():
	    user_uri = self.uri_ref(user.name, 'users')

	    self._graph.add((user_uri,    RDF.type,        T['User']))
            self._graph.add((user_uri,    T['Name'],       Literal(user.name)))
            self._graph.add((user_uri,    T['Terminal'],   Literal(user.terminal)))
            self._graph.add((user_uri,    T['Host'],       Literal(user.host)))
            self._graph.add((user_uri,    T['Started'],    Literal(float(user.started))))

        self._graph.serialize(URI, format='n3')
