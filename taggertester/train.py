#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Train a part-of-speech tagger from provided training and props files."""

import os
import subprocess32

from .config import DATA_DIR_NAME, PATH_TO_DATA_DIR, PATH_TO_JAR

def train_tagger(props_file, heap_size='-mx1g', jar_path=PATH_TO_JAR,):
    """Train a part-of-speech tagger from a provided properties file."""
    # we assume that the props file is in the 'datafiles' directory
    path_to_props = os.path.join(PATH_TO_DATA_DIR, props_file)
    subprocess32.call(['java', heap_size, '-classpath', jar_path,
                       'edu.stanford.nlp.tagger.maxent.MaxentTagger',
                       '-props', path_to_props])
