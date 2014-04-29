# -*- coding: utf-8 -*-
from __future__ import absolute_import
import warnings
import argparse

from trifle.utils.cli       import prompt, prompt_pass, prompt_bool, prompt_choices
from trifle.managers.parser import ArgumentParser
from trifle.managers.group  import Group

class Command(object):
    """
    Base class for creating commands.
    """

    option_list = []

    @property
    def description(self):
        description = self.__doc__ or ''
        return description.strip()

    def add_option(self, option):
        """
        Adds Option to option list.
        """
        self.option_list.append(option)

    def get_options(self):
        """
        By default, returns self.option_list. Override if you
        need to do instance-specific configuration.
        """
        return self.option_list

    def create_parser(self, *args, **kwargs):

        parser = ArgumentParser(*args, **kwargs)

        for option in self.get_options():
            if isinstance(option, Group):
                if option.exclusive:
                    group = parser.add_mutually_exclusive_group(
                        required=option.required,
                    )
                else:
                    group = parser.add_argument_group(
                        title=option.title,
                        description=option.description,
                    )
                for opt in option.get_options():
                    group.add_argument(*opt.args, **opt.kwargs)
            else:
                parser.add_argument(*option.args, **option.kwargs)

        parser.set_defaults(func_handle=self.handle)

        return parser

    def handle(self, app, *args, **kwargs):
        """
        Handles the command with given app. Default behaviour is to call within
        a test request context.
        """
        #with app.test_request_context():
        return self.run(*args, **kwargs)

    def run(self):
        """
        Runs a command. This must be implemented by the subclass. Should take
        arguments as configured by the Command options.
        """
        raise NotImplementedError

    def prompt(self, name, default=None):
        warnings.warn_explicit(
            "Command.prompt is deprecated, use prompt() function instead")

        prompt(name, default)

    def prompt_pass(self, name, default=None):
        warnings.warn_explicit(
            "Command.prompt_pass is deprecated, use prompt_pass() function "
            "instead")

        prompt_pass(name, default)

    def prompt_bool(self, name, default=False):
        warnings.warn_explicit(
            "Command.prompt_bool is deprecated, use prompt_bool() function "
            "instead")

        prompt_bool(name, default)

    def prompt_choices(self, name, choices, default=None):
        warnings.warn_explicit(
            "Command.choices is deprecated, use prompt_choices() function "
            "instead")

        prompt_choices(name, choices, default)
