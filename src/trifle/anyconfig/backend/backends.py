#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
from itertools import groupby
from operator import methodcaller

import trifle.anyconfig.backend.base as Base
import trifle.anyconfig.backend.ini_ as BINI
import trifle.anyconfig.backend.json_ as BJSON
import trifle.anyconfig.backend.xml_ as BXML
import trifle.anyconfig.backend.yaml_ as BYAML
import trifle.anyconfig.utils as U
import pkg_resources

# cmp is missing in python >= 3.0.
try:
    cmp
except NameError:
    def cmp(a, b):
        return (a > b) - (a < b)


_CPs = [p for p in [BINI.IniConfigParser, BJSON.JsonConfigParser,
                    BYAML.YamlConfigParser, BXML.XmlConfigParser,
                    ] if p.supports()]

for e in pkg_resources.iter_entry_points("anyconfig_backends"):
    try:
        _CPs.append(e.load())
    except ImportError:
        continue


def cmp_cps(lhs, rhs):
    """Compare config parsers by these priorities.
    """
    return cmp(lhs.priority(), rhs.priority())


def fst(tpl):
    """
    >>> fst((0, 1))
    0
    """
    return tpl[0]


def snd(tpl):
    """
    >>> snd((0, 1))
    1
    """
    return tpl[1]


def groupby_key(xs, kf):
    return groupby(sorted(xs, key=kf), key=kf)


def uniq(iterable):
    """
    >>> uniq([1, 2, 3, 1, 2])
    [1, 2, 3]
    """
    acc = []
    for x in iterable:
        if x not in acc:
            acc.append(x)

    return acc


def list_parsers_by_type(cps=_CPs):
    """
    :return: List (generator) of (config_type, [config_parser])
    """
    return ((t, sorted(p, key=methodcaller("priority"))) for t, p in
            groupby_key(cps, methodcaller("type")))


def _list_xppairs(xps):
    return sorted((snd(xp) for xp in xps), key=methodcaller("priority"))


def list_parsers_by_extension(cps=_CPs):
    """
    :return: List (generator) of (config_ext, [config_parser])
    """
    cps_by_ext = U.concat(([(x, p) for x in p._extensions] for p in cps))

    return ((x, _list_xppairs(xps)) for x, xps in groupby_key(cps_by_ext, fst))


def find_by_file(config_file, cps=_CPs):
    """
    Find config parser by file's extension.

    :param config_file: Config file path
    """
    ext = U.get_file_extension(config_file)
    for x, ps in list_parsers_by_extension(cps):
        if x == ext:
            return ps[-1]

    return None


def find_by_type(cptype, cps=_CPs):
    """
    Find config parser by file's extension.

    :param cptype: Config file's type
    """
    for t, ps in list_parsers_by_type(cps):
        if t == cptype:
            return ps[-1]

    return None


def list_types(cps=_CPs):
    """List available config types.
    """
    return sorted(uniq(t for t, ps in list_parsers_by_type(cps)))

# vim:sw=4:ts=4:et:
