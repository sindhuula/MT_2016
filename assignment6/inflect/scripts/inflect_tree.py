#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Outputs a fully inflected version of a lemmatized test set (provided on STDIN). 
If training data is provided, it will use a unigram model to select the form.

usage: cat LEMMA_FILE | python inflect
       [-t TRAINING_PREFIX] [-l LEMMA_SUFFIX] [-w WORD_SUFFIX]
"""

import argparse
import codecs
import sys
import os
from collections import defaultdict
from itertools import izip
from tree import DepTree

PARSER = argparse.ArgumentParser(description="Inflect a lemmatized corpus")
PARSER.add_argument("-t", type=str, default="data/train", help="training data prefix")
PARSER.add_argument("-l", type=str, default="lemma", help="lemma file suffix")
PARSER.add_argument("-w", type=str, default="form", help="word file suffix")
PARSER.add_argument("-d", type=str, default="data/dtest", help="tag file suffix for dev/test")
PARSER.add_argument("-tt", type=str, default="tree", help="word file suffix")

args = PARSER.parse_args()

# Python sucks at UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout) 
sys.stdin = codecs.getreader('utf-8')(sys.stdin) 

def combine(a, b): return '%s.%s' % (a, b)
def combine3(a, b, c): return '%s.%s.%s' % (a, b, c)

def tree_inflections(lemma1,lemma2, lemma3, words,tree):
    '''
    if LEMMAST.has_key(combine3(lemma2,words[int(tree[0])-1],tree[1])):
        #print "1"
        return sorted(LEMMAST[combine3(lemma2,words[int(tree[0])-1],tree[1])].keys(), lambda x,y: cmp(LEMMAST[combine3(lemma2,words[int(tree[0])-1],tree[1])][y], LEMMAST[combine3(lemma2,words[int(tree[0])-1],tree[1])][x]))

    elif LEMMAST.has_key(combine(lemma2,tree[1])):
       # print "2"
        return sorted(LEMMAST[combine(lemma2,tree[1])].keys(), lambda x,y: cmp(LEMMAST[combine(lemma2,tree[1])][y], LEMMAST[combine(lemma2,tree[1])][x]))
    '''
    elif LEMMAS.has_key(combine3(lemma3,lemma1,lemma2)):
        #print "3"
        return sorted(LEMMAS[combine3(lemma3,lemma1,lemma2)].keys(), lambda x,y: cmp(LEMMAS[combine3(lemma3,lemma1,lemma2)][y], LEMMAS[combine3(lemma3,lemma1,lemma2)][x]))
    
    elif LEMMAS.has_key(combine(lemma1,lemma2)):
        #print "4"
        return sorted(LEMMAS[combine(lemma1,lemma2)].keys(), lambda x,y: cmp(LEMMAS[combine(lemma1,lemma2)][y], LEMMAS[combine(lemma1,lemma2)][x]))

    elif LEMMAS.has_key(lemma2):
        #print "6"
        return sorted(LEMMAS[lemma2].keys(), lambda x,y: cmp(LEMMAS[lemma2][y], LEMMAS[lemma2][x]))
    #print "7"
    return [lemma2]
        
def best_inflection(lemma1,lemma2, lemma3, words, tree):
    return tree_inflections(lemma1,lemma2,lemma3, words, tree)[0]

if __name__ == '__main__':

    # Build a simple unigram model on the training data
    LEMMAS = defaultdict(defaultdict)
    LEMMAST = defaultdict(defaultdict)
    count = defaultdict(int)
    total = 0
    sents = 0
    if args.t:
        def utf8read(file): return codecs.open(file, 'r', 'utf-8')
        # Build the LEMMAS hash, a two-level dictionary mapping lemmas to inflections to counts
        for words, lemmas, trees in izip(utf8read(combine(args.t, args.w)), utf8read(combine(args.t, args.l)),utf8read(combine(args.t, args.tt))):
            prev = "<BOS>"
            prev_prev = "<BOS>"
            word_dict = words.rstrip().lower().split()
            lemma_dict = lemmas.rstrip().lower().split()
            tree_dict = trees.rstrip().split()
            sents += 1
            for word, lemma, tree in izip(word_dict, lemma_dict,tree_dict):
                split_tree = tree.split('/')
                count[(1,lemma)] += 1 
                count[(2,combine(prev,lemma))] += 1
                count[(3,combine3(prev_prev,prev,lemma))] += 1
                total += 1
                if int(split_tree[0]) == 0:
                      LEMMAST[combine(lemma,split_tree[1])][word] = LEMMAS[combine(lemma,split_tree[1])].get(word,0) + 1
                      
                else:
                      LEMMAST[combine3(lemma,lemma_dict[int(split_tree[0])-1],split_tree[1])][word] = LEMMAST[combine3(lemma,lemma_dict[int(split_tree[0])-1],split_tree[1])].get(word,0) + 1
                
                LEMMAS[lemma][word] = LEMMAS[lemma].get(word,0) + 1
                LEMMAS[combine(prev,lemma)][word] = LEMMAS[combine(prev,lemma)].get(word,0) + 1
                LEMMAS[combine3(prev_prev,prev,lemma)][word] = LEMMAS[combine3(prev_prev,prev,lemma)].get(word,0) + 1
                prev_prev = prev
                prev = lemma
    # Choose the most common inflection for each word and output them as a sentence
    tree_file = [line.rstrip() for line in utf8read(combine(args.d,args.tt))]
    index = 0
    for line in sys.stdin:
        prev = "<BOS>"
        prev_prev = "<BOS>"
        tree_line = tree_file[index].lower().split()
        result = []
        words = line.rstrip().lower().split()
        for word in words:
            tree = tree_line.pop().split('/')
            result.append(best_inflection(prev,word,prev_prev,words,tree))
            prev_prev = prev
            prev = word
        print ' '.join(result)
        index += 1
