#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import taggertester

from nltk.tag.stanford import StanfordPOSTagger

def main():
    # define a training file
    tf = taggertester.TrainingFile(file_name='uyghurtagger.train',
                                   separator='_')
    # split the training file into groups
    tf.split_groups()

    #for g in xrange(1, tf.num_groups+1): # uncomment to do all groups
    for g in [1]: # do just the first group (for testing)
        # make the index a pretty string with leading zero
        str_idx = str(g).rjust(2,'0')
        # specify a filename for the test and train files
        test_file = 'test_{}.txt'.format(str_idx)
        train_file = 'train_{}.train'.format(str_idx)

        # link the two files in a FilePair object
        fp = taggertester.FilePair(idx=g, testfile=test_file,
                                   trainfile=train_file,
                                   separator='_')
        # write a properties file
        fp.write_props()
        # train a new tagger using the property file
        taggertester.train_tagger(props_file=fp.props_name)

        # locate the new model in the filesystem
        model_name = os.path.join(taggertester.PATH_TO_DATA_DIR,
                                  'model_{}.model'.format(str_idx))

        # initialize a Stanford Tagger which calls our model
        uy = StanfordPOSTagger(model_name, taggertester.PATH_TO_JAR)

        # tag a sentence using the tagger.
        tagged = uy.tag('Men méning mantini yégenlikimni bilimen .'.split())
        # print the tagged sentence
        for w in tagged:
            print u'{}_{} '.format(w[0], w[1]),

if __name__ == '__main__':
    main()
