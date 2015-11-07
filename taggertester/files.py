#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

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
        # one-digit numbers should be prefaced with leading zeros
        self.idx = str(idx).rjust(2, '0')

    def __str__(self):
        """Provide a human-readable representation of the object.

           Returns two measurements of the size of the training file:
               number of sentences and total number of tokens.
        """
        summary = 'TrainingFile with {} total sentences and {} total tokens'
        return summary.format(len(self.contents()),
                sum([len(i[1].split(' ')) for i in self.contents()]))

class TestingOutputFile(object):
    """POS Tagging Results file, the accuracy of which we want to measure."""

    def __init__(self):
        pass
