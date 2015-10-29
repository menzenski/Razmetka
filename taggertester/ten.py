#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Split a provided training file into ten parts for cross-validation."""

import random
import subprocess32

def chunks(l, n=10):
    """Yield successive n-length chunks from l.

    Parameters
    ----------
      l : iterable -- the thing we're splitting into chunks.
      n : int      -- the length of chunk we want to produce.
      """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def create_groups(number_of_items, n=10):
    """Create n random groups of equal length.

    Parameters
    ----------
      number_of_items : int -- size of the thing we're splitting
      n : int               -- the number of groups we want
    """
    items = range(1, number_of_items)
    group_length = number_of_items / n
    random.shuffle(items)
    return chunks(l=items, n=group_length)

def train_single_tagger(jar_path, props_file):
    """Train a single POS tagger from a props file."""
    subprocess32.call(
        ['java', '-mx1g', '-classpath', jar_path,
         'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-props',
         props_file])
