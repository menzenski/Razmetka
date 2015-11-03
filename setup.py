#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='taggertester',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Train and test a part-of-speech tagger',
    install_requires=['subprocess32'],
    url='https://github.com/menzenski/tagger-tester',
    author='Matt Menzenski',
    author_email='matt.menzenski@gmail.com'
    )
