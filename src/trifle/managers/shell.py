# -*- coding: utf-8 -*-
from __future__ import absolute_import
import code
from termcolor import colored

from trifle.managers.command import Command
from trifle.managers.option  import Option
from trifle.managers.group   import Group
from trifle.store            import Store

class Shell(Command):
    """
    Runs a Python shell inside Trifle context.

    :param banner: banner appearing at top of shell when started
    :param make_context: a callable returning a dict of variables
                         used in the shell namespace. By default
                         returns a dict consisting of just the app.
    :param use_bpython: use BPython shell if available, ignore if not.
                        The BPython shell can be turned off in command
                        line by passing the **--no-bpython** flag.
    :param use_ipython: use IPython shell if available, ignore if not.
                        The IPython shell can be turned off in command
                        line by passing the **--no-ipython** flag.
    """

    banner = ''

    help = description = 'Runs a Python shell inside Trifle context.'

    def __init__(self, banner=None, make_context=None, use_ipython=True,
                use_bpython=True):

        self.banner = banner or self.banner
        self.use_ipython = use_ipython
        self.use_bpython = use_bpython

        #if make_context is None:
        #   import Queue              as queue
        #   import trifle.raft.store  as rstore
        #   import trifle.raft.server as rserver
        #   import trifle.raft.tcp    as rchannel
        #   import trifle.raft.log    as rlog 

        #   store = Store()
	#   q1 = queue.Queue()                                                               
	#   q2 = queue.Queue()                                                               
        #   s1 = rserver.Server(q1, 6181, [])
        #   s2 = rserver.Server(q2, 6182, [])
        #   s1.peers = {s1.uuid: ('127.0.0.1', 6181), s2.uuid: ('127.0.0.1', 6182)}
        #   s2.peers = {s1.uuid: ('127.0.0.1', 6181), s2.uuid: ('127.0.0.1', 6182)}
        #   s1.start()
        #   s2.start()

        #   print colored('store', attrs=['bold']), \
        #           '= Store()', \
        #           colored("(%s statements)" % len(store.graph),'cyan')
        #   print colored('server1', attrs=['bold']), \
        #           '= Server(queue1, %s, [])'%'6181', \
	#	   colored("(uuid: %s)" % s1.uuid,'cyan')
        #   print colored('server2', attrs=['bold']), \
        #           '= Server(queue2, %s, [])'%'6182', \
	#	   colored("(uuid: %s)" % s2.uuid,'cyan')

        #   make_context = lambda: dict(
        #           server1=s1,
        #           server2=s2,
        #           rlog=rlog,
        #           queue1=q1,
        #           queue2=q2,
        #           channel=rchannel,
        #           rstore=rstore,
        #           store=store)

        #self.make_context = make_context

    def get_options(self):
        return (
            Option('--no-ipython',
                action="store_true",
                dest='no_ipython',
                default=not(self.use_ipython)),
            Option('--no-bpython',
                action="store_true",
                dest='no_bpython',
                default=not(self.use_bpython))
        )

    def get_context(self):
        """
        Returns a dict of context variables added to the shell namespace.
        """
        return self.make_context()

    def run(self, no_ipython, no_bpython):
        """
        Runs the shell.  If no_bpython is False or use_bpython is True, then
        a BPython shell is run (if installed).  Else, if no_ipython is False or
        use_python is True then a IPython shell is run (if installed).
        """

        context = self.get_context()

        if not no_bpython:
            # Try BPython
            try:
                from bpython import embed
                embed(banner=self.banner, locals_=context)
                return
            except ImportError:
                pass

        if not no_ipython:
            # Try IPython
            try:
                try:
                    # 0.10.x
                    from IPython.Shell import IPShellEmbed
                    ipshell = IPShellEmbed(banner=self.banner)
                    ipshell(global_ns=dict(), local_ns=context)
                except ImportError:
                    # 0.12+
                    from IPython import embed
                    embed(banner1=self.banner, user_ns=context)
                return
            except ImportError:
                pass

        

        # Use basic python shell
        code.interact(self.banner, local=context)
