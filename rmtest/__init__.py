# pylint: disable=missing-docstring, invalid-name, duplicate-code

import unittest
import os
import contextlib
from redis import ResponseError

from rmtest.disposableredis import DisposableRedis
from rmtest import config

REDIS_MODULE_PATH_ENVVAR = 'REDIS_MODULE_PATH'
REDIS_PATH_ENVVAR = 'REDIS_PATH'
REDIS_PORT_ENVVAR = 'REDIS_PORT'


class BaseModuleTestCase(unittest.TestCase):
    """
    You can inherit from this base class directly. The server, port, and module
    settings can be defined either directly via the config module (see the
    config.py file), or via the rmtest.config file in the current directoy (i.e.
    of the process, not the file), or via environment variables.
    """
    _server = None
    _client = None

    def tearDown(self):
        if hasattr(self, '_server'):
            self._server.stop()
            self._server = None
            self._client = None

        super(BaseModuleTestCase, self).tearDown()

    @property
    def server(self):
        self._ensure_server()
        return self._server

    @property
    def client(self):
        self._ensure_server()
        return self._client

    def spawn_server(self, **kwargs):
        if hasattr(self, '_server'):
            raise Exception('Server already spawned!')
        self._ensure_server(**kwargs)

    def restart_and_reload(self):
        self._server.dump_and_reload(restart_process=True)
        self._client = self._server.client()

    def _ensure_server(self, **kwargs):
        if getattr(self, '_server', None):
            return
        self._server = self.redis(**kwargs)
        self._server.start()
        self._client = self._server.client()

    @property
    def module_args(self):
        """
        Module-specific arguments required
        """
        return []

    @property
    def server_args(self):
        """
        Server-specific arguments required
        """
        return {}

    @property
    def is_external_server(self):
        """
        :return: True if the connected-to server is already launched
        """
        return config.REDIS_PORT

    def redis(self, **redis_args):
        """
        Return a connection to a server, creating one or connecting to an
        existing server.
        """
        if not config.REDIS_MODULE:
            raise Exception('No module specified. Use config file or environment!')
        redis_args.update(self.server_args)
        redis_args.update(
            {'loadmodule': [config.REDIS_MODULE] + self.module_args})
        return DisposableRedis(port=config.REDIS_PORT, path=config.REDIS_BINARY, **redis_args)

    def cmd(self, *args, **kwargs):
        return self.client.execute_command(*args, **kwargs)

    def assertOk(self, oks, msg=None):
        if isinstance(oks, (bytes, bytearray)):
            self.assertEqual(b"OK", oks, msg)
        else:
            self.assertEqual("OK", oks, msg)

    def assertCmdOk(self, cmd, *args, **kwargs):
        self.assertOk(self.cmd(cmd, *args, **kwargs))

    def assertExists(self, r, key, msg=None):
        self.assertTrue(r.exists(key), msg)

    def assertNotExists(self, r, key, msg=None):
        self.assertFalse(r.exists(key), msg)

    def retry_with_reload(self):
        return self.client.retry_with_rdb_reload()

    @contextlib.contextmanager
    def assertResponseError(self, msg=None):
        """
        Assert that a context block with a redis command triggers a redis error response.

        For Example:

            with self.assertResponseError():
                r.execute_command('non_existing_command')
        """

        try:
            yield
        except ResponseError:
            pass
        else:
            self.fail("Expected redis ResponseError " + (msg or ''))


def ModuleTestCase(module_path, redis_path='redis-server', module_args=None):
    """
    DEPRECATED. Use base class directly.

    Inherit your test class from the class generated by calling this function
    module_path is where your module.so resides, override it with REDIS_MODULE_PATH in env
    redis_path is the executable's path, override it with REDIS_PATH in env
    redis_port is an optional port for an already running redis
    module_args is an optional tuple or list of arguments to pass to the module on loading
    """

    module_path = config.REDIS_MODULE if config.REDIS_MODULE else module_path
    redis_path = config.REDIS_BINARY if config.REDIS_BINARY else redis_path
    fixed_port = config.REDIS_PORT if config.REDIS_PORT else None
    port = fixed_port if fixed_port else None

    # If we have module args, create a list of arguments
    loadmodule_args = module_path \
        if not module_args else [module_path] + list(module_args)

    class _ModuleTestCase(BaseModuleTestCase):
        _loadmodule_args = loadmodule_args

        @property
        def module_args(self):
            args = super(_ModuleTestCase, self).module_args
            if module_args:
                args += module_args

        def redis(self, **kwargs):
            return DisposableRedis(port=port, path=redis_path,
                                   loadmodule=self._loadmodule_args, **kwargs)

    return _ModuleTestCase
