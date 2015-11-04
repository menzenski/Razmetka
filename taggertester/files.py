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

    def __init__(self, file_name, separator="_"):
        """Initialize the file object.

           Parameters
           ----------
             file_name (str) : name of the file, with extension
             separator (str) : character used in the file to separate
               words from their POS tags, e.g.:
                   'table/NN' -- separator is '/'
                   'table_NN' -- separator is '_'
        """
        self.file_name = file_name
        self.sep = separator

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
            self.raw_content = f.readlines()

        return [(idx, ln[:-1]) for idx, ln in enumerate(self.raw_content)]

class TrainingFile(BaseFile):
    """Training file consisting of hand-tagged sentences."""

    def __init__(self, file_name, separator='_', idx=1):
        BaseFile.__init__(self, file_name, separator)
        # one-digit numbers should be prefaced with leading zeros
        self.idx = str(idx).rjust(2, '0')

    def write(self):
        """Write the training file to disk."""
        pass

class TestingOutputFile(object):
    """POS Tagging Results file, the accuracy of which we want to measure."""

    def __init__(self):
        pass
