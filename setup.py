#! /usr/bin/env python
"""Jarvis project install script."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="jarvis",
    version="0.1",
    description="Just A Rather Very Intelligent System",
    long_description=open("README.md").read(),
    author="c-square",
    url="https://github.com/c-square/evorepo-common",
    packages=["jarvis"],
    scripts=["scripts/jarvis"],
    requires=[]
)
