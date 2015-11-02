#! /usr/bin/env python
"""EvoRepo project install script."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="evorepo",
    version="0.1",
    description="",
    long_description=open("README.md").read(),
    author="c-square",
    url="https://github.com/c-square/evorepo-common",
    packages=["evorepo"],
    scripts=["scripts/evorepo"],
    requires=[]
)
