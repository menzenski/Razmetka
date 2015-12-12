#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provide corpora objects for part-of-speech tagging and segmentation."""

import codecs
import os

from nltk.corpus.reader import TaggedCorpusReader

from .util import to_unicode_or_bust

class TaggedSegmentedCorpusReader(TaggedCorpusReader):
    """A corpus reader for texts which are both tagged and segmented."""

    def __init__(self, *args, **kwargs):
        """Initialize the TaggedSegmentedCorpusReader object.

           Parameters
           ----------
             arg (type) :
        """
        super(TaggedSegmentedCorpusReader, self).__init__(*args, **kwargs)
