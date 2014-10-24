#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LICENSE') as f:
    license = f.read()

with open('README.rst') as f:
    description = f.read()

setup(
    name='sharegg',
    version='0.1.0',
    author='Alexandre Vicenzi',
    author_email='vicenzi.alexandre@gmail.com',
    maintainer='Alexandre Vicenzi',
    maintainer_email='vicenzi.alexandre@gmail.com',
    packages=['sharegg'],
    url='https://github.com/alexandrevicenzi/sharegg',
    bugtrack_url='https://github.com/alexandrevicenzi/sharegg/issues',
    license=license,
    description='Sharegg',
    long_description=description,
    keywords='',
    platforms='',
    install_requires=['Flask', 'unirest'],
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS',
          'Operating System :: Microsoft',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Topic :: System',
          'Topic :: Utilities',
          ],
)
