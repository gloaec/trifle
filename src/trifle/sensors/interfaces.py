# -*- coding: utf-8 -*-
import netifaces
import os

from trifle.base.sensor import BaseSensor, RDF, T, Literal

class InterfacesSensor(BaseSensor):

    path = "interfaces"

    def pull(self):
        for interface in netifaces.interfaces():
            interface_uri = self.uri_ref(interface)
	    self.graph.add((interface_uri, RDF.type, T['Interface']))
	    self.graph.add((interface_uri, T['Name'], Literal(interface)))
	    for t, addresses in netifaces.ifaddresses(interface).items():
                classname = {
                        2 : 'IPv4Address', 
                	17: 'MACAddress', 
                	10: 'IPv6Address'}[t]
                for i, address in enumerate(addresses):
                    address_uri = os.path.join(interface_uri, 'addresses',
                            classname, str(i))
                    if t in [2,10]:
                        self.graph.add((address_uri, RDF.type, T['IPAddress']))
                        version = {
                                2: '4',
                                10: '6'
                        }[t]
                        self.graph.add((address_uri, T['Version'], Literal(version)))
                        self.graph.add((address_uri, T['Type'], Literal("IPv%s"%version)))
                    elif t == 17:
                        self.graph.add((address_uri, T['Type'], Literal('MAC')))
                    self.graph.add((address_uri, RDF.type, T[classname]))
                    for k, v in address.items():
                        dataproperty = {
                            'addr'     : 'Address',
                            'peer'     : 'Peer',
                            'broadcast': 'Broadcast',
                            'netmask'  : 'NetMask'}[k]
                        self.graph.add((address_uri, T[dataproperty], Literal(v)))
		    self.graph.add((address_uri,   T['locates'],   interface_uri))
		    self.graph.add((interface_uri, T['locatedAt'], address_uri))

    queries = {
        "Interfaces with MAC addresses": """
            SELECT ?InterfaceName ?MACAddress
            WHERE {
                ?Interface a t:Interface .
                ?Interface t:Name ?InterfaceName .
                ?MAC a t:MACAddress .
                ?MAC t:locates ?Interface .
                ?MAC t:Address ?MACAddress .
            }
	""",
 
        "Interfaces with all addresses": """
            SELECT ?InterfaceName ?Address ?Type
            WHERE { 
                ?Interface a t:Interface . 
                ?Interface t:Name ?InterfaceName .
                ?Location t:locates ?Interface .
                ?Location t:Type ?Type .
		?Location t:Address ?Address .
            }
            """,
 
        "Interfaces with all IP addresses/netmasks/broadcasts": """
            SELECT ?InterfaceName ?IPVersion ?Address ?NetMask ?Broadcast
            WHERE { 
                ?Interface a t:Interface . 
                ?Interface t:Name ?InterfaceName .
                ?Location t:locates ?Interface .
                ?Location a t:IPAddress .
                ?Location t:Version ?IPVersion .
		?Location t:Address ?Address .
                ?Location t:NetMask ?NetMask .
                ?Location t:Broadcast ?Broadcast .
            }
            """
    }
