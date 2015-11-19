#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tag.stanford import StanfordPOSTagger

from .config import DATA_DIR_NAME, PATH_TO_DATA_DIR, PATH_TO_JAR
from .files import TrainingFile, write_to_directory
from .files import to_unicode_or_bust as tuob
from .tag import FilePair

class TaggerTester(object):
    """Collection of files for training/testing part-of-speech taggers."""

    def __init__(self, file_name, language='', test_name='test_',
                 train_name='train_', model_name='model_',
                 props_name='props_', separator='_', ws_delim=True,
                 starting_idx=1, number_of_groups=10, encoding='utf-8'):
        """Initialize the test suite.

           Parameters
           ----------
             file_name (str) : name of the input_file, with extension
             language (str) : the language of the file (e.g., 'Uyghur')
             test_name (str) : prefix for naming/saving test files
             train_name (str) : prefix for naming/saving training files
             model_name (str) : prefix for naming/saving tagger files
             props_name (str) : prefix for naming/saving property files
             separator (basestring) : the character used in the file
               to separate words from their part-of-speech tags, e.g.:
                   'table/NN' -- separator is '/'
                   'table_NN' -- separator is '_'
             ws_delim (boolean) : is the file already whitespace-delimited?
               if the answer is 'yes', then True, e.g.:
                   Tursun_Npr ._PUNCT
               if the answer is 'no', then False, e.g.:
                   Tursun_Npr._PUNCT
             starting_idx (int) : number at which group numbering will start
             number_of_groups (int) : number of groups that the file will
               be split into for cross-validation
             encoding (str) : encoding of the input file
        """
        self.file_name = file_name
        self.language = language
        self.test_name = test_name
        self.train_name = train_name
        self.model_name = model_name
        self.props_name = props_name
        self.sep = tuob(separator)
        self.ws_delim = ws_delim
        self.starting_idx = starting_idx
        self.number_of_groups = number_of_groups
        self.encoding = encoding
        # list to organize ancillary files
        self.files = []

    def contents(self, file_name=None):
        """Return the contents of the main file."""
        if file_name is None:
            file_name = self.file_name
        pass

    def groups(self):
        """Return random groupings of sentences in the main file."""
        pass

    def estimate_tagger_accuracy(self, as_percent=True, verbose=False):
        """"""
        pass

class SentencePair(object):
    """Pair of sentences: one tagged by hand, one by a POS tagger."""

    def __init__(self, hand_tagged_sentence, language='', idx=1,
                 separator='_'):
        """Initialize the object.

           Parameters
           ----------
             hand_tagged_sentence (list) OR (unicode / str) : a sentence
               which has been tagged by hand (i.e., it belongs to part of
               the original training file which was set aside to serve as a
               test set)
             language (str) : the language of the pair (e.g., 'Uyghur')
             idx (int / str) : the index of this sentence in the original
               (complete) training file
             separator (str) : the character which serves to separate
               words from their part-of-speech tags (likely '_' or '/')
        """
        if isinstance(idx, int):
            self.idx = str(idx).rjust(2, '0')
        if isinstance(idx, basestring):
            self.idx = idx
        if isinstance(hand_tagged_sentence, basestring):
            self.hand_tagged = tuob(hand_tagged_sentence).split()
        if isinstance(hand_tagged_sentence, list):
            self.hand_tagged = [tuob(w) for w in hand_tagged_sentence]
        self.language = language
        self.sep = tuob(separator)
        # to be populated when the sentence is tagged by the tagger
        self.auto_tagged = self.strip_training_tags(self.hand_tagged)

    def __str__(self):
        """String representation of the SentencePair object."""
        summary = '{} object in the {} language, consisting of {} tokens.'
        return summary.format(
                type(self).__name__, self.language,
                len(self.hand_tagged)
                )

    def strip_training_tags(self, sentence=None, sep=None):
        """Remove the part-of-speech tags from a test sentence."""
        if sentence is None:
            sentence = self.hand_tagged
        if sep is None:
            sep = self.sep
        return [w.split(sep, 1)[0] for w in sentence]

    def tag(self, model_name, sentence=None, jarpath=PATH_TO_JAR):
        """Tag a sentence by calling the StanfordPOSTagger.

           Parameters
           ----------
             model_name (str) : name of the tagger model which will be used
               to tag the sentence. Located in the DATA_DIR, most likely.
             sentence (list) : the sentence to be tagged.
             jarpath (filepath) : path to the stanford-postagger.jar file
        """
        if sentence is None:
            sentence = self.auto_tagged
        self.auto_tagged = StanfordPOSTagger(
                model_name, jarpath).tag(sentence)
        return self.auto_tagged

    def compare_sentences(self, hand_tagged=None, auto_tagged=None):
        """Compare the hand-tagged original to the auto-tagged sentence.

           Parameters
           ----------
             auto_tagged (list) : list of 2-tuples comprised of word + tag
               for the words in the original hand_tagged sentence
        """
        if hand_tagged is None:
            hand_tagged = self.hand_tagged
        if auto_tagged is None:
            auto_tagged = self.auto_tagged
        if len(auto_tagged) == len(hand_tagged):
            print u'HAND TAGGED:'
            for idx, w in enumerate(hand_tagged):
                print u'\t{}\t{}'.format(idx, w)
            print u'AUTO TAGGED:'
            for idx, w in enumerate(auto_tagged):
                print u'\t{}\t{}_{}'.format(idx, w[0], w[1])

    def comparison(self, idx=1, hand_tagged=None, auto_tagged=None):
        """Return a tuple containing index and tagging result accuracy.

           Returns
           -------
             (tuple) : 2-tuple structured like the following:
                 (134, [1, 1, 1, 0, 1, 1])
              in which the first item is the index of this sentence in the
              original (complete) hand-tagged training file and the second
              item is a list of length len(hand_tagged). In each position in
              the list a 1 indicates that the tagger output matches the
              hand-tagged input perfectly, and a 0 indicates that it doesn't.
        """
        if hand_tagged is None:
            hand_tagged = self.hand_tagged
        if auto_tagged is None:
            auto_tagged = self.auto_tagged
        if len(hand_tagged) == len(auto_tagged):
            rl = [1 if hand_tagged[i] == u'{}{}{}'.format(
                    auto_tagged[i][0], self.sep, auto_tagged[i][1]) else 0
                    for i in xrange(0, len(hand_tagged))]
            return (idx, rl)
        else:
            return (idx, "Sentence lengths don't match!")

    def accuracy(self, in_list=None, as_percent=False):
        """Return a tuple representing tagger accuracy on the sentence.

           Parameters
           ----------
             in_list (list) : the list to measure
             as_percent (boolean) : return a percent value instead of a tuple

           Returns
           -------
             if as_percent is True:
               a float rounded to two decimal places, e.g., 79.74
             if as_percent is False:
               a 2-tuple in which the first int represents the number of
               matches and the second int represents the number of misses
        """
        if in_list is None:
            in_list = self.comparison()[1]
        if as_percent == False:
            return in_list.count(1), in_list.count(0)
        else:
            # calculate the percentage
            pct = float(in_list.count(1)) / len(in_list) * 100
            # return percentage to two decimal places
            return float('{0:.2f}'.format(pct))
