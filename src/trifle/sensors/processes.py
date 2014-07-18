# -*- coding: utf-8 -*-
import os
import psutil
import logging

from trifle.base.sensor import BaseSensor, RDF, T, Literal

URI = "file:///home/ghis/Workspace/trifle/src/trifle/ontologies/processes.n3"
logger = logging.getLogger('trifle')

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

	        self._graph.add((process_uri, RDF.type,        T['Process']))
                self._graph.add((process_uri, T['Name'],       Literal(p.name())))
                self._graph.add((process_uri, T['ProcessID'],  Literal(int(pid))))
                self._graph.add((process_uri, T['Command'],    Literal(' '.join(p.cmdline()))))
                self._graph.add((process_uri, T['Status'],     Literal(p.status())))
                self._graph.add((process_uri, T['Cwd'],        Literal(p.cwd())))
                self._graph.add((process_uri, T['Terminal'],   Literal(p.cwd())))
                self._graph.add((process_uri, T['CPUPercent'], Literal(float(p.cpu_percent()))))
                self._graph.add((process_uri, T['RAMPercent'], Literal(float(p.memory_percent()))))
                self._graph.add((process_uri, T['launchedBy'], user_uri))
                self._graph.add((process_uri, T['executedBy'], command_uri))

	        self._graph.add((user_uri,    RDF.type,        T['User']))
                self._graph.add((user_uri,    T['Name'],       Literal(p.username())))
                self._graph.add((user_uri,    T['launches'],   process_uri))

	        self._graph.add((command_uri, RDF.type,        T['Command']))
	        self._graph.add((command_uri, T['Binary'],     Literal(p.exe())))
	        self._graph.add((command_uri, T['Argument'],   Literal(' '.join(p.cmdline()[1:]))))
	        self._graph.add((command_uri, T['executes'],   process_uri))
	    except psutil.AccessDenied:
                logger.critical("AccessDenied: Are you root ?")
	    except psutil.NoSuchProcess:
		logger.warning("NoSuchProcess: %s"%pid)
	        self._graph.add((process_uri, RDF.type,        T['Process']))
                self._graph.add((process_uri, T['Status'],     Literal('zombie')))

        self._graph.serialize(URI, format='n3')
