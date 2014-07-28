# -*- coding: utf-8 -*-
import os
import psutil

from trifle.base.sensor import BaseSensor, RDF, T, Literal

class ServicesSensor(BaseSensor):

    path = "services"

    def pull(self):
        for interface in netifaces.interfaces():
            interface_uri = self.uri_ref(interface)
	    self.graph.add((interface_uri, RDF.type, T['Interface']))
	    print netifaces.ifaddresses(interface)
	    for t, addresses in netifaces.ifaddresses(interface).items():
                classname = {
                        2 : 'IPv4Address', 
			17: 'MACAdress', 
			10: 'IPv6Address'}[t]
                for i, address in enumerate(addresses):
		    address_uri = os.path.join(interface_uri, 'addresses',
                            classname, str(i))
		    self.graph.add((address_uri, RDF.type, T[classname]))
                    for k, v in address.items():
                        dataproperty = {
                            'addr'     : 'Address',
			    'peer'     : 'Peer',
			    'broadcast': 'Broadcast',
			    'netmask'  : 'NetMask'}[k]
		        self.graph.add((address_uri, T[dataproperty], Literal(v)))
