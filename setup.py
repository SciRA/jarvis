#! /usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="watson",
    version="0.1",
    description="",
    long_description=open("README.md").read(),
    author="Alexandru Coman",
    author_email="contact@alexcoman.com",
    url="https://github.com/alexandrucoman/watson",
    packages=["watson"],
    scripts=["scripts/watson"],
    requires=["redis"]
)
