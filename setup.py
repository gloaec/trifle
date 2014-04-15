#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

project = "trifle"

setup(
    name             = project,
    version          = "0.0.1",
    url              = "http://github.com/gloaec/%s" %project,
    license          = "GPLv3",
    author           = "Ghislain Loaec",
    author_email     = "gloaec@cadoles.com",
    maintainer       = "Ghislain Loaec",
    maintainer_email = "gloaec@cadoles.com",
    description      = "Context-Aware Configuration Management System",
    long_description = __doc__,
    package_dir      = {"":"src"},
    packages         = [project],
)

