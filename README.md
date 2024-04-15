# vkmtest

A simple nano-framework for testing valkey modules using python unit test, and a disposable ephemeral valkey subprocess.

## Example:

```py

import unittest
from vkmtest import ModuleTestCase

class MyTestCase(ModuleTestCase('../module.so', module_args = ('foo', 'bar'))):
            
    def testCmd(self):
        self.assertOk(self.cmd('mymodule.dosomething', 'foo', 'bar'))

if __name__ == '__main__':
    unittest.main()               
    
```

## Controlling parameters with Environment Variables

It is possible to control the path to the valkey server executable, the path to the module and an optional fixed port, from environment variables.

### VALKEY_MODULE_PATH

Controls the path to the module, either absolute, or relative to where the test resides.

### VALKEY_PATH

Controls the path to valkey-server. By default we assume it's in `$PATH`

### VALKEY_PORT

Causes the tests to run against a fixed valkey port instead of spawning ephemeral disposable valkey instances for each test. 

This is useful for debugging failures with `valkey-cli MONITOR`.

## VALKEY_DEBUGGER

Causes the tests to be run under a debugger (e.g. `valgrind`). The value to this
environment variable is the path to the debugger. Does not work if there are spaces
in the path.


## Installing from pypi

```sh
$ pip install vkmtest
```

## Installing from Git

1. Clone this repo

2. `sudo python setup.py install`
