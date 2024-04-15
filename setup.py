#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='vkmtest',
    version='1.0.0',
    description='Valkey Module Testing Utility',
    url='http://github.com/valkey-io/vkmtest',
    packages=find_packages(),
    install_requires=['valkey'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database',
        'Topic :: Software Development :: Testing'
    ]
)
