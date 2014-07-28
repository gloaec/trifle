# -*- coding: utf-8 -*-
from __future__ import absolute_import
import code
from termcolor import colored

from trifle.managers.command import Command
from trifle.managers.option  import Option
from trifle.managers.group   import Group

from trifle.sensors.interfaces import InterfacesSensor
from trifle.sensors.processes  import ProcessesSensor
from trifle.sensors.users      import UsersSensor

class Snapshot(Command):
    """
    Makes a context snapshot from various sensors

    """

    banner = ''

    help = description = 'Makes a context snapshot from various sensors'

    def __init__(self, banner=None):

        self.banner = banner or self.banner

    def get_options(self):
        return []

    def run(self):
        """
	Generate ontologies from sensors

        """

	InterfacesSensor().snapshot()
	ProcessesSensor().snapshot()
	UsersSensor().snapshot()


