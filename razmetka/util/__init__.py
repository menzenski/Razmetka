#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['to_unicode_or_bust']

__version__ = '0.0.1'
__author__ = 'Matthew Menzenski'
__author_email__ = 'menzenski@ku.edu'

def get_version():
    return __version__

from .corpus import TaggedSegmentedCorpusReader
from .util import to_unicode_or_bust
