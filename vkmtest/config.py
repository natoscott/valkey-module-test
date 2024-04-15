# pylint: disable=missing-docstring, invalid-name, too-few-public-methods

"""
Configuration file for determining port, path, etc. of Valkey. This is used
by all loaded tests.

This file exports three variables, VALKEY_BINARY which contains the executable
path for Valkey; VALKEY_MODULE which contains the path to the module to test,
and VALKEY_PORT which connects to an already-existent valkey server.

The `VALKEY_PATH`, `VALKEY_MODULE_PATH`, and `VALKEY_PORT` environment variables
can all be used to override these settings.
"""

import os
try:
    from configparser import ConfigParser, NoOptionError, NoSectionError
except ImportError:
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError


class ConfigVar(object):
    def __init__(self, env, prop, default=None):
        self.env = env
        self.prop = prop
        self.default = default
        self.value = default


cfg = ConfigParser()
cfg.read(['vmktest.config'])

entries = {
    'path': ConfigVar('VALKEY_PATH', 'executable', 'valkey-server'),
    'module': ConfigVar('VALKEY_MODULE_PATH', 'module'),
    'port': ConfigVar('VALKEY_PORT', 'existing_port')
}

for _, ent in entries.items():
    try:
        ent.value = cfg.get('server', ent.prop)
    except (NoOptionError, NoSectionError):
        pass

    # Override from environment
    if ent.env in os.environ:
        ent.value = os.environ[ent.env]


VALKEY_BINARY = entries['path'].value
VALKEY_MODULE = entries['module'].value
VALKEY_PORT = entries['port'].value
if VALKEY_PORT:
    VALKEY_PORT = int(VALKEY_PORT)
