#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# no slashes '/' in this name (they'll be added as necessary later)
MODEL_DIR_NAME = 'models'
"""Name of the directory where Morfessor models are located."""

# absolute path to the model directory
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(script_dir, os.pardir)
PATH_TO_MODEL_DIR = os.path.join(parent_dir, MODEL_DIR_NAME)
"""Absolute path to the directory where Morfessor models are located."""
