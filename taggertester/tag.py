#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess32

from nltk.tag.stanford import POSTagger

from . import TrainingFile

class TrainingSuite(object):
    """Collection of files for training and testing POS taggers."""

    def __init__(self, file_dict, separator='_'):
        """Initialize the TrainingSuite object.

           Parameters
           ----------
             file_dict (dict) : dictionary with the following structure:
               {
                    01: (test_01.txt, train_01.train),
                    02: (test_02.txt, train_02.train),
               }
             separator (str) : the character used to separate words
               from their POS tags in the training file and the output.
               Default is underscore '_'; slash '/' is also common.
        """
        self.all_files = file_dict
        self.sep = separator
