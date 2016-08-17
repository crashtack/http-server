# -*- coding: utf-8 -*-
"""Package implements a simple HTTP Response server."""
from setuptools import setup

setup(
    name="http-server",
    description="A Python implementation of a simple http echo client/server.",
    version=0.1,
    author="David Banks, Derek Hewitt",
    author_email="crashtack@gmail.com, derekmhewitt@gmail.com",
    license='MIT',
    py_modules=['client', 'server'],
    package_dir={'': 'src'},
    install_requires=[],
    extras_require={'test': ['pytest', 'pytest-watch', 'pytest-cov', 'tox']},
)
