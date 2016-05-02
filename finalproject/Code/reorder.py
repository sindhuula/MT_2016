#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Outputs a version where the phrases are re-ordered in SVO order
TODO Change the order within the phrase and improve reordering
"""

import argparse
import codecs
import sys
import os
from collections import defaultdict
from itertools import izip

PARSER = argparse.ArgumentParser(description="Reorder a set of sentences")
PARSER.add_argument("-t", type=str, default="data/train", help="training data prefix")
PARSER.add_argument("-d", type=str, default="data/dev", help="dev data prefix")
PARSER.add_argument("-w", type=str, default="es", help="spanish file")
PARSER.add_argument("-p", type=str, default="pos", help="tag file")
args = PARSER.parse_args()

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

def combine(a, b): return '%s.%s' % (a, b)
def reorder(line):
    print "blah"
    return "meh"
if __name__ == '__main__':

    if args.t:
        def utf8read(file): return codecs.open(file, 'r', 'utf-8')
        #Training Section
        #Incorrect_ordering = word, dep_tag pair
        #Correct ordering = word, dep_tag pair
        for words in izip(utf8read(combine(args.t, args.w))):
            word_dict = words.rstrip().lower().split()
            for word in izip(word_dict):
                print "yeah"
        #Dev Section
        # From the trained portion find out how the tags were re-ordered and try to replicate
        # Our program simply just exchanges the phrases
        print "Read the sentences"
        print "Read the tag files for the sentences"
        print "Shuffle phrases"
        print "Train set may actually help to identify the correct ordering of the words and give an idea about how to reshuffle the tags"
        print "Dev and test set need to use the training model to see how to get an output"
    # Choose the most common inflection for each word and output them as a sentence
    for line in sys.stdin:
        result = reorder(line)
        print ' '.join(result)


