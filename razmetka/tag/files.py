#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provide file objects for training and testing part-of-speech taggers."""

import codecs
import os

from nltk.corpus.reader import TaggedCorpusReader

from razmetka.util.util import to_unicode_or_bust

from . import ten
from .config import DATA_DIR_NAME

def write_to_directory(dir_name, file_name, a_string,
                       mode='w+', encoding='utf-8'):
    """Write a string to a file in a  subdirectory which may not exist yet."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(script_dir, os.pardir)
    dest_dir = os.path.join(parent_dir, dir_name)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass # destination directory already exists
    path_to_file = os.path.join(dest_dir, file_name)
    with codecs.open(path_to_file, mode=mode, encoding=encoding) as f:
        f.write(a_string)

class BaseFile(object):
    """Base file type from which training and testing files are derived."""

    def __init__(self, file_name, language='', separator='_', ws_delim=True,
                 number_of_groups=10, encoding='utf-8'):
        """Initialize the file object.

           Parameters
           ----------
             file_name (str) : name of the file, with extension
             language (str) : the language of the file (e.g., 'Uyghur')
             separator (basestring) : character used in the file to separate
               words from their part-of-speech tags, e.g.:
                   'table/NN' -- separator is '/'
                   'table_NN' -- separator is '_'
             ws_delim (boolean) : is the file already whitespace-delimited?
               if the answer is 'yes', then True. Example:
                   Tursun_Npr ._PUNCT
               if the answer is 'no', then False. Example:
                   Tursun_Npr._PUNCT
             number_of_groups (int) : the number of groups that the file
               will be split into (for cross-validation)
        """
        self.file_name = file_name
        self.language = language
        self.sep = separator
        self.ws_delim = ws_delim
        self.num_groups = number_of_groups
        self.enc = encoding

    def __str__(self):
        """Provide a human-readable representation of the object.

           Returns two measurements of the size of the training file:
               number of sentences and total number of tokens.
        """
        summary = '{} object in the {} language, consisting of ' \
                  '{} total sentences and {} total tokens.'
        return summary.format(
                type(self).__name__,
                self.language,
                len(self.contents()),
                sum([len(i[1].split(' ')) for i in self.contents()])
                )

    def contents(self):
        """Create a list of sentences from the provided file.

           The result list is structured as follows:
                [
                    (0, u'Sen_PN2si sening_PN2si.Gen ma...'),
                    (1, u'Sen_PN2si mantini_N-ACC yedim...'),
                    (2, u'Sen_PN2si manta_N yegenliking...'),
                ]
        """
        with codecs.open(self.file_name, mode='r+', encoding=self.enc) as f:
            return [(i, to_unicode_or_bust(l)[:-1]) for i, l in
                    enumerate(f.readlines())]

    def to_string(self):
        """Output the BaseFile object as a single unicode string."""
        return u"\n".join([i[1] for i in self.contents()])

    def write(self, save_name=None):
        """Write the training file to disk."""
        if save_name is None:
            save_name = DATA+DIRECTORY + self.file_name
        with codecs.open(save_name, mode='w+', encoding='utf-8') as stream:
            stream.write(self.to_string())

    def groups(self, num_of_groups=None):
        """Split the file into ten randomly assigned groups.

           Parameters
           ----------
             num_of_groups (int) : the number of groups to be formed
        """
        if num_of_groups is None:
            num_of_groups = self.num_groups
        return [g for g in ten.create_groups(len(self.contents()),
                                             n=num_of_groups)]

    def split_groups(self, num_of_groups=None, verbose=True):
        """Split the file into training and test files.

           Parameters
           ----------
             num_of_groups (int) : the number of groups to be formed
             verbose (Boolean) : print the contents of each file
               to the console (if True), or not (if False)
        """
        if num_of_groups is None:
            num_of_groups = self.num_groups
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

            if verbose == True:
                print u"{}\tTEST SENTENCES:".format(i-1)
                for s in test_sentences:
                    print u"\t{}\t{}".format(s[0], s[1])
                print u"\n\tTRAINING SENTENCES:"
                for s in train_sentences:
                    print u"\t{}\t{}".format(s[0], s[1])

            test_output = u'\n'.join([s[1] for s in test_sentences])
            write_to_directory(dir_name=DATA_DIR_NAME, file_name=test_name,
                               a_string=test_output)

            train_output = u'\n'.join([s[1] for s in train_sentences])
            write_to_directory(dir_name=DATA_DIR_NAME, file_name=train_name,
                               a_string=train_output)

            # add index and matching filenames to all_files dict
            # self.all_files[idx] = (test_name, train_name)
            i += 1

class TrainingFile(BaseFile):
    """Training file consisting of hand-tagged sentences."""

    def __init__(self, file_name, language='', separator='_', ws_delim=True,
            idx=1, number_of_groups=10, encoding='utf-8'):
        """Initialize the TrainingFile object.

           Parameters
           ----------
             idx (str) : index used to identify the subset of the original
               BaseFile.
        """
        BaseFile.__init__(self, file_name=file_name, language=language,
                separator=separator, ws_delim=ws_delim,
                number_of_groups=number_of_groups, encoding=encoding)
        # one-digit numbers should be prefaced with a leading zero
        self.idx = str(idx).rjust(2, '0')

class TestingOutputFile(BaseFile):
    """POS Tagging Results file, the accuracy of which we want to measure."""

    def __init__(self, file_name, separator='_', idx=1):
        """Initialize the TestingOutputFile object."""
        BaseFile.__init__(self, file_name, separator)
        # one-digit numbers should be prefaced with a leading zero
        self.idx = str(idx).rjust(2, '0')

class TTTaggedCorpusReader(TaggedCorpusReader):
    """NLTK TaggedCorpusReader"""

    def __init__(self, file_name, language='', separator='_', ws_delim=True,
                 number_of_groups=10, encoding='utf-8'):
        """Initialize the corpus reader."""
        TaggedCorpusReader.__init__(self, root='.', fileids=[file_name],
                                    sep=separator, encoding=encoding)
