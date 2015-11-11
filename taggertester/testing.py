#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tag.stanford import StanfordPOSTagger

from .config import DATA_DIR_NAME, PATH_TO_DATA_DIR
from .files import TrainingFile, write_to_directory
from .tag import FilePair

class TaggerTester(object):
    """Collection of files for training/testing part-of-speech taggers. """

    def __init__(self):
        """Initialize the test suite."""
        pass


class SentencePair(object):
    """Pair of sentences: one tagged by hand, one by a POS tagger."""

    def __init__(self, hand_tagged_sentence, auto_tagged_sentence,
                 separator='_'):
        """Initialize the object.

           Parameters
           ----------
             hand_tagged_sentence (unicode / str) : a sentence which has
               been tagged by hand (i.e., it belongs to part of the original
               training file which was set aside to serve as a test set)
             auto_tagged_sentence (list) : a sentence which has been tagged
               automatically by a part-of-speech tagger
             separator (str) : the character which serves to separate
               words from their part-of-speech tags (likely '_' or '/')
        """
        # split the hand-tagged sentence on whitespace, since the auto-tagged
        # sentence will already be split and we want them to match
        self.hand_tagged = hand_tagged_sentence.split()
        self.auto_tagged = auto_tagged_sentence
        self.sep = separator

    def strip_training_tags(self, sentence=None, sep=None):
        """Remove the part-of-speech tags from a test sentence."""
        if sentence == None:
            sentence = self.hand_tagged
        if sep == None:
            sep = self.sep
        return [w.split(sep, 1)[0] for w in sentence]
