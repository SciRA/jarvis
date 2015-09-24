#! /usr/bin/env python
"""ASCon (Web App Security Control) install script."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="watson",
    version="0.1",
    description="",
    long_description=open("README.md").read(),
    author="c-square",
    url="https://github.com/c-square/watson",
    packages=["watson"],
    scripts=["scripts/watson"],
    requires=["redis"]
)
