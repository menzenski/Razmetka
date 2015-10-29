#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Split a provided training file into ten parts for cross-validation."""

import random
import subprocess32

from .config import PATH_TO_JAR

def chunks(l, n=10):
    """Yield successive n-length chunks from l.

    Parameters
    ----------
      l : iterable -- the thing we're splitting into chunks.
      n : int      -- the number of chunks we want.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def create_groups(number_of_items, n=10):
    """Create n random groups of equal length."""
    items = range(1, number_of_items)
    random.shuffle(items)
    return chunks(l=items, n=n)

def train_single_tagger(props_file)
    """Train a single POS tagger from a props file."""
    subprocess32.call(
        ['java', '-mx1g', '-classpath', PATH_TO_JAR,
         'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-props',
         props_file])

if __name__ == '__main__':
    train_single_tagger('uyghurtagger.props')
