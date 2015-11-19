#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ['DATA_DIR_NAME', 'PATH_TO_DATA_DIR', 'PATH_TO_JAR',
           'TrainingFile', 'TestingOutputFile', 'FilePair',
           'TaggerTester', 'SentencePair', 'repeat_tagger_tests',
           'train_tagger']

__version__ = '0.0.1'
__author__ = 'Matthew Menzenski'
__author_email__ = 'menzenski@ku.edu'

def get_version():
    return __version__

from .config import DATA_DIR_NAME, PATH_TO_DATA_DIR, PATH_TO_JAR
from .files import TrainingFile, TestingOutputFile
from .tag import FilePair
from .testing import TaggerTester, SentencePair, repeat_tagger_tests
from .train import train_tagger
