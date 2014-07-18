# -*- coding: utf-8 -*-
import netifaces
import os

from trifle.base.sensor import BaseSensor, RDF, T, Literal

URI = "file:///home/ghis/Workspace/trifle/src/trifle/ontologies/interfaces.n3"

class InterfacesSensor(BaseSensor):

    _path = "interfaces"

    def pull(self):
        for interface in netifaces.interfaces():
            interface_uri = self.uri_ref(interface)
	    self._graph.add((interface_uri, RDF.type, T['Interface']))
	    for t, addresses in netifaces.ifaddresses(interface).items():
                classname = {
                        2 : 'IPv4Address', 
			17: 'MACAdress', 
			10: 'IPv6Address'}[t]
                for i, address in enumerate(addresses):
		    address_uri = os.path.join(interface_uri, 'addresses',
                            classname, str(i))
		    self._graph.add((address_uri, RDF.type, T[classname]))
                    for k, v in address.items():
                        dataproperty = {
                            'addr'     : 'Address',
			    'peer'     : 'Peer',
			    'broadcast': 'Broadcast',
			    'netmask'  : 'NetMask'}[k]
		        self._graph.add((address_uri, T[dataproperty], Literal(v)))
        self._graph.serialize(URI, format='n3')
