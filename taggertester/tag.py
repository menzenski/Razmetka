#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import subprocess32

from nltk.tag.stanford import StanfordPOSTagger

from .config import DATA_DIR_NAME, PATH_TO_DATA_DIR
from .files import write_to_directory

class FilePair(object):
    """Pair of files: one for training and one for testing."""

    def __init__(self, idx, testfile, trainfile, separator='_'):
        """Initialize the TrainingSuite object.

           Parameters
           ----------
             idx (int) : index number to keep files straight
             testfile (str) : filename containing the file to tag/test
             trainfile (str) : filename containing the training file
             separator (str) : the character used to separate words
               from their POS tags in the training file and the output.
               Default is underscore '_'; slash '/' is also common.
        """
        # one-digit numbers should be prefaced with a leading zero
        self.idx = str(idx).rjust(2, '0')
        self.testfile = testfile
        self.trainfile = trainfile
        self.props_name = 'props_{}.props'.format(self.idx)
        # self.all_files = file_dict
        self.sep = separator
        self.prop_template = (
            "model = {p_model}\n"
            "trainFile = {p_train_file}\n"
            "tagSeparator = {p_tag_separator}\n"
            "encoding = {p_encoding}\n"
            "verbose = {p_verbose}\n"
            "verboseResults = {p_verbose_results}\n"
            "tokenize = {p_tokenize}\n"
            "arch = {p_arch}\n"
            "learnClosedClassTags = {p_learn_closed_class_tags}\n"
            "closedClassTagThreshold = {p_closed_class_tag_threshold}\n"
            )

    def write_props(self, props_name=None, model=None, train_file=None,
            tag_separator=None, encoding="UTF-8", verbose="true",
            verbose_results="true", tokenize="false", arch="generic",
            learn_closed_class_tags='', closed_class_tag_threshold=5):
        """Write a props file to disk."""
        if props_name == None:
            props_name = self.props_name
        if model == None:
            model_name = 'model_{}.model'.format(self.idx)
            model = os.path.join(PATH_TO_DATA_DIR, model_name)
        if train_file == None:
            train_file = os.path.join(PATH_TO_DATA_DIR, self.trainfile)
        if tag_separator == None:
            tag_separator = self.sep
        output_string = self.prop_template.format(
            p_model=model, p_train_file=train_file,
            p_tag_separator=tag_separator, p_encoding=encoding,
            p_verbose=verbose, p_verbose_results=verbose_results,
            p_tokenize=tokenize, p_arch=arch,
            p_learn_closed_class_tags=learn_closed_class_tags,
            p_closed_class_tag_threshold=closed_class_tag_threshold
            )
        write_to_directory(dir_name=DATA_DIR_NAME, file_name=props_name,
                           a_string=output_string)
