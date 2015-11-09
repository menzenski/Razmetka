#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provide file objects for training and testing part-of-speech taggers."""

import codecs

from . import ten

def to_unicode_or_bust(obj, encoding='utf-8'):
    ## function written by Kumar McMillan ( http://farmdev.com/talks/unicode )
    """Ensure that an object is unicode."""
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

class BaseFile(object):
    """Base file type from which training and testing files are derived."""

    def __init__(self, file_name, separator="_", ws_delim=True):
        """Initialize the file object.

           Parameters
           ----------
             file_name (str) : name of the file, with extension
             separator (str) : character used in the file to separate
               words from their POS tags, e.g.:
                   'table/NN' -- separator is '/'
                   'table_NN' -- separator is '_'
             ws_delim (boolean) : is the file already whitespace-delimited?
               if yes, then True. Example:
                   Tursun_Npr ._PUNCT
               if no, then False. Example:
                   Tursun_Npr._PUNCT
        """
        self.file_name = file_name
        self.sep = separator
        self.ws_delim = ws_delim
        ## dict to organize files used for training and testing
        self.all_files = {}

    def contents(self):
        """Create a list of sentences from the provided file.

           The result list is structured as follows:
                [
                    (0, u'Sen_PN2si sening_PN2si.Gen ma...'),
                    (1, u'Sen_PN2si mantini_N-ACC yedim...'),
                    (2, u'Sen_PN2si manta_N yegenliking...'),
                ]
        """
        with open(self.file_name) as f:
            self.raw_content = [to_unicode_or_bust(l) for l in f.readlines()]

        return [(idx, ln[:-1]) for idx, ln in enumerate(self.raw_content)]

    def to_string(self):
        """Output the BaseFile object as a single unicode string."""
        return u"\n".join([i[1] for i in self.contents()])

    def write(self, save_name=None):
        """Write the training file to disk."""
        if save_name == None:
            save_name = self.file_name
        with codecs.open(save_name, mode='w+', encoding='utf-8') as stream:
            stream.write(self.to_string())

    def groups(self, num_of_groups=10):
        """Split the file into ten randomly assigned groups.

           Parameters
           ----------
             num_of_groups (int) : the number of groups to be formed
        """
        return [g for g in ten.create_groups(len(self.contents()),
                                             n=num_of_groups)]

    def split_groups(self, num_of_groups=10):
        """Split the file into training and test files."""
        # test_01 is the test file containing group 01
        # train_01 is the training file containing all groups EXCEPT 1
        i = 1
        group_list = self.groups()
        while i <= num_of_groups:
            idx = str(i).rjust(2, '0')
            test_name = "test_{}.txt".format(idx)
            train_name = "train_{}.train".format(idx)

            # form lists (remember that they're zero-indexed!)
            test_list = group_list[i-1]
            # first produce a nested list of non-i lists
            train_list_nested = [group_list[j] for j in range(
                len(group_list)) if j != i-1]
            # then collapse nested list into flat list
            train_list = [k for l in train_list_nested for k in l]

            test_sentences = []
            train_sentences = []
            for position, sentence in self.contents():
                if position in test_list:
                    test_sentences.append((position, sentence))
                else:
                    train_sentences.append((position, sentence))
            with codecs.open(test_name, 'w+', encoding='utf-8') as test:
                test.write(u"\n".join([s[1] for s in test_sentences]))
            with codecs.open(train_name, 'w+', encoding='utf-8') as train:
                train.write(u"\n".join([s[1] for s in train_sentences]))
            # add index and matching filenames to all_files dict
            self.all_files[idx] = (test_name, train_name)
            i += 1

class TrainingFile(BaseFile):
    """Training file consisting of hand-tagged sentences."""

    def __init__(self, file_name, separator='_', idx=1):
        """Initialize the TrainingFile object.

           Parameters
           ----------
             idx (str) : index used to identify the subset of the original
               BaseFile.
        """
        BaseFile.__init__(self, file_name, separator)
        # one-digit numbers should be prefaced with a leading zero
        self.idx = str(idx).rjust(2, '0')

    def __str__(self):
        """Provide a human-readable representation of the object.

           Returns two measurements of the size of the training file:
               number of sentences and total number of tokens.
        """
        summary = 'TrainingFile with {} total sentences and {} total tokens'
        return summary.format(len(self.contents()),
                sum([len(i[1].split(' ')) for i in self.contents()]))

class TestingOutputFile(BaseFile):
    """POS Tagging Results file, the accuracy of which we want to measure."""

    def __init__(self, file_name, separator='_', idx=1):
        """Initialize the TestingOutputFile object."""
        BaseFile.__init__(self, file_name, separator)
        # one-digit numbers should be prefaced with a leading zero
        self.idx = str(idx).rjust(2, '0')

