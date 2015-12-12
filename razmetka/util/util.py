#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provide functions for handling special characters."""

def to_unicode_or_bust(obj, encoding='utf-8'):
    """Ensure that an object is unicode.

       This function was written by Kumar McMillan:
       ( http://farmdev.com/talks/unicode )
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
