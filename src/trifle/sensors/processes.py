# -*- coding: utf-8 -*-
import os
import psutil
import logging; logger = logging.getLogger('trifle')

from trifle.base.sensor import BaseSensor, RDF, T, Literal

# A considérer :
# p.open_files() -> Déduire les permissions/ownership/manager
# p.connections() -> laddr=('10.0.0.1', 48776), raddr=('93.186.135.91', 80), status='ESTABLISHED'

class ProcessesSensor(BaseSensor):

    def pull(self):
        for pid in psutil.get_pid_list():
            process_uri = self.uri_ref(str(pid), 'processes')
            try:
                p = psutil.Process(pid)

	        user_uri    = self.uri_ref(p.username(), 'users')
	        command_uri = self.uri_ref(str(pid),     'commands')

	        self.graph.add((process_uri, RDF.type,        T['Process']))
                self.graph.add((process_uri, T['Name'],       Literal(p.name())))
                self.graph.add((process_uri, T['ProcessID'],  Literal(int(pid))))
                self.graph.add((process_uri, T['Command'],    Literal(' '.join(p.cmdline()))))
                self.graph.add((process_uri, T['Status'],     Literal(p.status())))
                self.graph.add((process_uri, T['Cwd'],        Literal(p.cwd())))
                self.graph.add((process_uri, T['Terminal'],   Literal(p.cwd())))
                self.graph.add((process_uri, T['CPUPercent'], Literal(float(p.cpu_percent()))))
                self.graph.add((process_uri, T['RAMPercent'], Literal(float(p.memory_percent()))))
                self.graph.add((process_uri, T['launchedBy'], user_uri))
                self.graph.add((process_uri, T['executedBy'], command_uri))

	        self.graph.add((user_uri,    RDF.type,        T['User']))
                self.graph.add((user_uri,    T['Name'],       Literal(p.username())))
                self.graph.add((user_uri,    T['launches'],   process_uri))

	        self.graph.add((command_uri, RDF.type,        T['Command']))
	        self.graph.add((command_uri, T['Binary'],     Literal(p.exe())))
	        self.graph.add((command_uri, T['Argument'],   Literal(' '.join(p.cmdline()[1:]))))
	        self.graph.add((command_uri, T['executes'],   process_uri))
	    except psutil.AccessDenied:
                logger.critical("AccessDenied: Are you root ?")
	    except psutil.NoSuchProcess:
		logger.warning("NoSuchProcess: %s"%pid)
	        self.graph.add((process_uri, RDF.type,        T['Process']))
                self.graph.add((process_uri, T['Status'],     Literal('zombie')))

    queries = {
        "All processes": """
            SELECT ?UserName ?PID ?TTY ?Command ?ProcessName ?Status
            WHERE {
                ?Process a t:Process .
                ?Process t:ProcessID ?PID .
                ?Process t:launchedBy ?User .
                ?Process t:Terminal ?TTY .
                ?Process t:Command ?Command .
                ?Process t:Name ?ProcessName .
		?Process t:Status ?Status .
                ?User t:Name ?UserName .
            }
	""",

        "Zombie processes": """
            SELECT ?PID ?Command ?ProcessName
            WHERE {
                ?Process a t:Process .
		?Process t:Status "zombie" .
                ?Process t:ProcessID ?PID .
                ?Process t:Command ?Command .
                ?Process t:Name ?ProcessName .
            }
	"""
    }
