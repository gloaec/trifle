#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

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
    packages         = [
        'rdflib',
        'rdflib/extras',
        'rdflib/plugins',
        'rdflib/plugins/parsers',
        'rdflib/plugins/parsers/pyRdfa',
        'rdflib/plugins/parsers/pyRdfa/transform',
        'rdflib/plugins/parsers/pyRdfa/extras',
        'rdflib/plugins/parsers/pyRdfa/host',
        'rdflib/plugins/parsers/pyRdfa/rdfs',
        'rdflib/plugins/parsers/pyMicrodata',
        'rdflib/plugins/serializers',
        'rdflib/plugins/sparql',
        'rdflib/plugins/sparql/results',
        'rdflib/plugins/stores',
        'rdflib/tools'
        #project,
        #"%s.managers" % project,
        #"%s.utils"    % project
        #"%s.server" % project,
        #"%s.utils"    % project
    ],
    classifiers      = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    platforms        = 'any',
    entry_points     = {
      'console_scripts': [ "%s = %s:main" % (project, project) ],
    },
)

