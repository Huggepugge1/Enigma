#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="enigma",
    version="0.0.1",
    description="CTF library",
    author="Hugo Lindström",
    author_email="huggepugge1@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["nltk", "factordb-pycli"]
)
