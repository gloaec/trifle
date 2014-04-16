# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys
import logging

from trifle.managers import Manager
from trifle.store import Store

config = {}

def main(argv=None, prog=None, **kwargs):
    manager = Manager()
    config  = get_config()
    logging.basicConfig(level=logging.DEBUG)
    manager.run()

def get_config(filename="trifle.conf"):
    config = {}
    return config

if __name__ == "__main__":
    main(sys.argv[1:])

