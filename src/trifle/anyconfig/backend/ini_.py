#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
from trifle.anyconfig.compat import StringIO, configparser, iteritems
from trifle.anyconfig.globals import LOGGER as logging

import trifle.anyconfig.backend.base as Base
import trifle.anyconfig.parser as P

import os.path
import sys


SUPPORTED = True  # It should be available w/ python dist always.

_SEP = ','


# FIXME: Ugly
def _parse(v, sep=_SEP):
    """
    :param v: A string represents some value to parse
    :param sep: separator between values

    >>> _parse(r'"foo string"')
    'foo string'
    >>> _parse("a, b, c")
    ['a', 'b', 'c']
    >>> _parse("aaa")
    'aaa'
    """
    if (v.startswith('"') and v.endswith('"')) or \
            (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    elif sep in v:
        return [P.parse(x) for x in P.parse_list(v)]
    else:
        return P.parse(v)


def _to_s(v, sep=_SEP):
    if isinstance(v, list):
        return ", ".join(x for x in v)
    else:
        return str(v)


def _load_impl(config_fp, sep=_SEP, **kwargs):
    """
    :param config_fp: File or file-like object provides ini-style conf
    :return: Dict or dict-like object represents config values
    """
    config = dict()

    # Optional arguements for configparser.SafeConfigParser{,readfp}
    kwargs_0 = Base.mk_opt_args(("defaults", "dict_type", "allow_no_value"),
                                kwargs)
    kwargs_1 = Base.mk_opt_args(("filename", ), kwargs)

    try:
        try:
            parser = configparser.SafeConfigParser(**kwargs_0)
        except TypeError:
            # It seems ConfigPaser.*ConfigParser in python 2.6 does not support
            # 'allow_no_value' option parameter, and TypeError will be thrown.
            kwargs_0 = Base.mk_opt_args(("defaults", "dict_type"), kwargs)
            parser = configparser.SafeConfigParser(**kwargs_0)

        parser.readfp(config_fp, **kwargs_1)

        if parser.defaults():
            config["DEFAULT"] = dict()

            for k, v in iteritems(parser.defaults()):
                config["DEFAULT"][k] = _parse(v, sep)

        for s in parser.sections():
            config[s] = dict()

            for k, v in parser.items(s):
                config[s][k] = _parse(v, sep)

    except Exception:
        logging.warn(sys.exc_info()[-1])

    return config


def mk_lines_g(data):
    has_default = "DEFAULT" in data

    def is_inherited_from_default(k, v):
        return has_default and data["DEFAULT"].get(k, None) == v

    for sect, params in iteritems(data):
        yield "[%s]\n" % sect

        for k, v in iteritems(params):
            if sect != "DEFAULT" and is_inherited_from_default(k, v):
                continue

            yield "%s = %s\n" % (k, _to_s(v))

        yield "\n"  # put an empty line just after each sections.


class IniConfigParser(Base.ConfigParser):
    _type = "ini"
    _extensions = ["ini"]
    _supported = SUPPORTED

    _load_opts = ["defaults", "dict_type", "allow_no_value", "filename"]

    @classmethod
    def load_impl(cls, config_fp, **kwargs):
        """
        :param config_fp:  Config file object
        :param kwargs: configparser specific optional keyword parameters

        :return: dict object holding config parameters
        """
        return _load_impl(config_fp, sep=_SEP, **kwargs)

    @classmethod
    def dumps_impl(cls, data, **kwargs):
        """
        :param data: Data to dump :: dict
        :param config_path: Dump destination file path
        :param kwargs: backend-specific optional keyword parameters :: dict

        :return: string represents the configuration
        """
        return '\n'.join(l for l in mk_lines_g(data))

# vim:sw=4:ts=4:et:
