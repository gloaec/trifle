# -*- coding: utf-8 -*-
import os
import psutil

from trifle.base.sensor import BaseSensor, RDF, T, Literal

class UsersSensor(BaseSensor):

    def pull(self):
        for user in psutil.users():
	    user_uri = self.uri_ref(user.name, 'users')

	    self.graph.add((user_uri,    RDF.type,        T['User']))
            self.graph.add((user_uri,    T['Name'],       Literal(user.name)))
            self.graph.add((user_uri,    T['Terminal'],   Literal(user.terminal)))
            self.graph.add((user_uri,    T['Host'],       Literal(user.host)))
            self.graph.add((user_uri,    T['Started'],    Literal(float(user.started))))
