# -*- coding: utf-8 -*-
from __future__ import absolute_import

from trifle.managers.command import Command
from trifle.managers.option  import Option
from trifle.managers.group   import Group
from trifle.raft.server      import make_server

class RaftServer(Command):
    """
    Runs the Raft development server for agents

    :param host: server host
    :param port: server port
    :param use_debugger: if False, will no longer use Werkzeug debugger.
                         This can be overriden in the command line
                         by passing the **-d** flag.
    :param use_reloader: if False, will no longer use auto-reloader.
                         This can be overriden in the command line by
                         passing the **-r** flag.
    :param threaded: should the process handle each request in a separate
                     thread?
    :param processes: number of processes to spawn
    :param passthrough_errors: disable the error catching. This means that the server will die on errors but it can be useful to hook debuggers in (pdb etc.)
    :param options: :func:`werkzeug.run_simple` options.
    """

    help = description = 'Runs the Raft development server for agents'

    def __init__(self, host='0.0.0.0', port=8080, use_debugger=True,
                 use_reloader=True, threaded=False, processes=1,
                 passthrough_errors=False, **options):

        self.port = port
        self.host = host
        self.use_debugger = use_debugger
        self.use_reloader = use_reloader
        self.server_options = options
        self.threaded = threaded
        self.processes = processes
        self.passthrough_errors = passthrough_errors

    def get_options(self):

        options = (
            Option('-t', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('--threaded',
                   dest='threaded',
                   action='store_true',
                   default=self.threaded),

            Option('--processes',
                   dest='processes',
                   type=int,
                   default=self.processes),

            Option('--passthrough-errors',
                   action='store_true',
                   dest='passthrough_errors',
                   default=self.passthrough_errors),
        )

        if self.use_debugger:
            options += (Option('-d', '--no-debug',
                               action='store_false',
                               dest='use_debugger',
                               default=self.use_debugger),)

        else:
            options += (Option('-d', '--debug',
                               action='store_true',
                               dest='use_debugger',
                               default=self.use_debugger),)

        if self.use_reloader:
            options += (Option('-r', '--no-reload',
                               action='store_false',
                               dest='use_reloader',
                               default=self.use_reloader),)

        else:
            options += (Option('-r', '--reload',
                               action='store_true',
                               dest='use_reloader',
                               default=self.use_reloader),)

        return options

    def handle(self, app, host, port, use_debugger, use_reloader,
               threaded, processes, passthrough_errors):
        # we don't need to run the server in request context
        # so just run it directly

        server = make_server()
