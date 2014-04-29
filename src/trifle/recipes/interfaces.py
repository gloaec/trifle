# -*- coding: utf-8 -*-
import netifaces
import subprocess
import re

def pull():
    for interface in netifaces.interfaces():
        info = netiface.ifadresses(interface)
        
    
