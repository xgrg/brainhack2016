#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='kandu',
      version='1.1.1',
      packages=['kandu', 'kandu.web'],
      scripts=['bin/kandu_server'],
      install_requires=['tornado','requests','scandir'],
      include_package_data=True
      )
