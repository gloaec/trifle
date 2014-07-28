# -*- coding: utf-8 -*-
import subprocess
import re

from trifle.sensors.interfaces import InterfacesSensor
from trifle.sensors.processes import ProcessesSensor
from trifle.sensors.users import UsersSensor

def getHostname():
    cmd = 'hostname 2>&1'
    exc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return exc.stdout

def getServices():
    cmd = 'service --status-all 2>&1'
    exc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    services = []
    for line in exc.stdout:
         info = re.search('\[\s?([+-\??])\s?\]\s+(.*)', line, re.IGNORECASE)
         if info:
            status  = {'+': True, '-': False, '?': None}[info.group(1)]
            name    = info.group(2).strip()
            services.append({ 'name': name, 'status': status })
    return services
