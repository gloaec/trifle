#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Public APIs of anyconfig module.
"""
import trifle.anyconfig.globals as G
import trifle.anyconfig.mergeabledict as M
import trifle.anyconfig.backend.backends as Backends
import trifle.anyconfig.backend.json_ as BJ
import trifle.anyconfig.parser as P
import trifle.anyconfig.utils as U

# pylint: disable=W0611
# Import some global constants will be re-exported:
from trifle.anyconfig.mergeabledict import MS_REPLACE, MS_NO_REPLACE, \
    MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES
# pylint: enable=W0611

# pylint: disable=C0103
# Re-export:
list_types = Backends.list_types
getLogger = G.get_logger

# aliases:
container = M.MergeableDict
logging = G.LOGGER
# pylint: enable=W0611


def set_loglevel(level):
    """
    :param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    logging.setLevel(level)


def find_loader(config_path, forced_type=None):
    """
    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    :return: ConfigParser-inherited class object
    """
    if forced_type is not None:
        cparser = Backends.find_by_type(forced_type)
        if not cparser:
            logging.error(
                "No parser found for given type: " + forced_type
            )
            return None
    else:
        cparser = Backends.find_by_file(config_path)
        if not cparser:
            logging.error(
                "No parser found for given file: " + config_path
            )
            return None

    logging.debug("Using config parser of type: " + cparser.type())
    return cparser


def single_load(config_path, forced_type=None, **kwargs):
    """
    Load single config file.

    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    cparser = find_loader(config_path, forced_type)
    if cparser is None:
        return None

    logging.info("Loading: " + config_path)
    return cparser.load(config_path, **kwargs)


def multi_load(paths, forced_type=None, merge=MS_DICTS, marker='*', **kwargs):
    """
    Load multiple config files.

    The first argument `paths` may be a list of config file paths or
    a glob pattern specifying that. That is, if a.yml, b.yml and c.yml are in
    the dir /etc/foo/conf.d/, the followings give same results::

      multi_load(["/etc/foo/conf.d/a.yml", "/etc/foo/conf.d/b.yml",
                  "/etc/foo/conf.d/c.yml", ])

      multi_load("/etc/foo/conf.d/*.yml")

    :param paths: List of config file paths or a glob pattern to list paths
    :param forced_type: Forced configuration parser type
    :param merge: Strategy to merge config results of multiple config files
        loaded. see also: anyconfig.mergeabledict.MergeableDict.update()
    :param marker: Globbing markerer to detect paths patterns
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    assert merge in MERGE_STRATEGIES, "Invalid merge strategy: " + merge

    if marker in paths:
        paths = U.sglob(paths)

    config = container()
    for path in paths:
        if marker in path:  # Nested patterns like ['*.yml', '/a/b/c.yml'].
            conf_updates = multi_load(path, forced_type, merge, marker,
                                      **kwargs)
        else:
            conf_updates = single_load(path, forced_type, **kwargs)

        config.update(conf_updates, merge)

    return config


def load(path_specs, forced_type=None, merge=MS_DICTS, marker='*', **kwargs):
    """
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs:
        Configuration file path or paths or its pattern such as '/a/b/*.json'
    :param forced_type: Forced configuration parser type
    :param merge: Merging strategy to use
    :param marker: Globbing marker to detect paths patterns
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if marker in path_specs or U.is_iterable(path_specs):
        return multi_load(path_specs, forced_type, merge, marker, **kwargs)
    else:
        return single_load(path_specs, forced_type, **kwargs)


def loads(config_content, forced_type=None, **kwargs):
    """
    :param config_content: Configuration file's content
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if forced_type is None:
        return P.parse(config_content)

    cparser = find_loader(None, forced_type)
    if cparser is None:
        return P.parse(config_content)

    return cparser.loads(config_content, **kwargs)


def _find_dumper(config_path, forced_type=None):
    """
    Find configuration parser to dump data.

    :param config_path: Output filename
    :param forced_type: Forced configuration parser type
    :return: ConfigParser-inherited class object
    """
    cparser = find_loader(config_path, forced_type)

    if cparser is None or not getattr(cparser, "dump", False):
        logging.warn(
            "Dump method not implemented. Fallback to JsonConfigParser"
        )
        cparser = BJ.JsonConfigParser()

    return cparser


def dump(data, config_path, forced_type=None, **kwargs):
    """
    Save `data` as `config_path`.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param config_path: Output filename
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    """
    dumper = _find_dumper(config_path, forced_type)

    logging.info("Dumping: " + config_path)
    dumper.dump(data, config_path, **kwargs)


def dumps(data, forced_type, **kwargs):
    """
    Return string representation of `data` in forced type format.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Backend-specific string representation for the given data
    """
    return _find_dumper(None, forced_type).dumps(data, **kwargs)


# vim:sw=4:ts=4:et:
