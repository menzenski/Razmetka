#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# absolute path to the Stanford POS Tagger Java .jar file
PATH_TO_JAR = '/usr/share/stanford-postagger/stanford-postagger.jar'

# no slashes '/' in this name (they'll be added as necessary later)
DATA_DIR_NAME = 'datafiles'

# absolute path to the data directory
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(script_dir, os.pardir)
PATH_TO_DATA_DIR = os.path.join(parent_dir, DATA_DIR_NAME)
