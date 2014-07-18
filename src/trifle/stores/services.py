# -*- coding: utf-8 -*-
from __future__ import absolute_import
from termcolor import colored

from trifle.sensors import getServices

class Services(object):

    def __init__(self):
        self.refresh()   

    def refresh(self):
        self.services = getServices()

    def __repr__(self):
        p = []
        for service in self.services:
            pstatus = {True: 'on', False: 'off', None: 'unknown'}[service['status']]
            pcolor  = {True: 'green', False: 'red', None: 'grey'}[service['status']]
            p.append(" ".join(["%40s" % service['name'], colored(pstatus, pcolor, attrs=['bold'])]))
        return "\n".join(p)
