#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['MODEL_DIR_NAME', 'PATH_TO_MODEL_DIR']

__version__ = '0.0.1'
__author__ = 'Matt Menzenski'
__author_email__ = 'menzenski@ku.edu'

def get_version():
    return __version__

from .config import MODEL_DIR_NAME, PATH_TO_MODEL_DIR
