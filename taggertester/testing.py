#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tag.stanford import StanfordPOSTagger

from .config import DATA_DIR_NAME, PATH_TO_DATA_DIR
from .files import TrainingFile, write_to_directory
from .tag import FilePair

class TestSuite(object):
    """Collection of files for training/testing part-of-speech taggers. """

    def __init__(self, tagged_file, separator='_',
                 number_of_groups=10, ws_delim=True, by_morphemes=False):
        """Initialize the test suite."""
        self.tagged_file = tagged_file
        self.sep = separator
        self.number_of_groups = number_of_groups
        self.ws_delim = ws_delim
