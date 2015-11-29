#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Brill Tagger classes."""

import codecs
import os
import random

from nltk.tag import brill
from nltk.tag.brill_trainer import BrillTaggerTrainer
from nltk.tag.sequential import RegexpTagger, UnigramTagger, BigramTagger, \
                                TrigramTagger

from . import ten
from .config import DATA_DIR_NAME
from .files import to_unicode_or_bust as tuob
from .files import TTTaggedCorpusReader

class TTBrillTaggerTrainer(object):
    """A trainer for tbl taggers."""

    def __init__(self, file_name, language='', separator='_', ws_delim=True,
                 number_of_groups=10, train_size=0.65, max_rules=300,
                 min_score=3):
        """Construct a Brill tagger from baseline tagger and templates."""
        self.tcr = TTTaggedCorpusReader(file_name=file_name,
                                        language=language,
                                        separator=separator,
                                        ws_delim=ws_delim)
        self.num_groups = number_of_groups
        self.dev_size = len(self.tcr.sents())
        self.train_size = train_size
        self.max_rules = max_rules
        self.min_score = min_score
        self.tagged_data_list = [[(w.lower(), t) for w, t in s]
                                   for s in self.tcr.tagged_sents()]

    def train(self, templates=None, verbose=True):
        """Train a new Brill tagger."""
        if templates is None:
            templates = brill.nltkdemo18()

        random.seed(len(self.tagged_data_list))
        random.shuffle(self.tagged_data_list)
        cutoff = int(self.dev_size * self.train_size)

        training_data = self.tagged_data_list[:cutoff]
        test_data = self.tagged_data_list[cutoff:self.dev_size]

        # very simple regular expression tagger
        regex_tagger = RegexpTagger([
            (r'^-?[0-9]+(.[0-9]+)?$', 'PUNCT'),
            (r'.*', 'N')
            ])
        if verbose == True:
            print "Regular expression tagger accuracy:\n{}\n".format(
                    regex_tagger.evaluate(test_data))

        # unigram tagger
        unigram_tagger = UnigramTagger(train=training_data,
                                       backoff=regex_tagger)
        if verbose == True:
            print "Unigram tagger accuracy:\n{}\n".format(
                    unigram_tagger.evaluate(test_data))

        # bigram tagger
        bigram_tagger = BigramTagger(train=training_data,
                                     backoff=unigram_tagger)
        if verbose == True:
            print "Bigram tagger accuracy:\n{}\n".format(
                    bigram_tagger.evaluate(test_data))

        # trigram tagger
        trigram_tagger = TrigramTagger(train=training_data,
                                       backoff=bigram_tagger)
        if verbose == True:
            print "Trigram tagger accuracy:\n{}\n".format(
                    trigram_tagger.evaluate(test_data))

        # first iteration
        trainer = BrillTaggerTrainer(initial_tagger=trigram_tagger,
                                     templates=templates)
        brill_tagger = trainer.train(train_sents=training_data,
                                     max_rules=self.max_rules,
                                     min_score=self.min_score)
        if verbose == True:
            print "Initial Brill tagger accuracy:\n{}\n".format(
                    brill_tagger.evaluate(test_data))

        # folding
        for i in range(0, self.num_groups):
            # random splitting
            random.seed(len(self.tagged_data_list))
            random.shuffle(self.tagged_data_list)
            cutoff = int(self.dev_size * self.train_size)

            training_data = self.tagged_data_list[:cutoff]
            test_data = self.tagged_data_list[cutoff:self.dev_size]

            brill_tagger = trainer.train(train_sents=training_data,
                                         max_rules=self.max_rules,
                                         min_score=self.min_score)
            if verbose == True:
                print "Brill tagger accuracy, fold {}:\n{}\n".format(
                        i+1, brill_tagger.evaluate(test_data))

    def compare_templates(self):
        for i, t in enumerate([brill.nltkdemo18(), brill.nltkdemo18plus(),
                               brill.brill24(), brill.fntbl37()]):
            print "\nTEMPLATE {}==================\n".format(i)
            self.train(templates=t)

class TTBrillTagger(brill.BrillTagger):
    pass

