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
from nltk.probability import (ConditionalFreqDist, ConditionalProbDist,
                              LidstoneProbDist)

PARSER = argparse.ArgumentParser(description="Inflect a lemmatized corpus")
PARSER.add_argument("-t", type=str, default="data/train", help="training data prefix")
PARSER.add_argument("-l", type=str, default="lemma", help="lemma file suffix")
PARSER.add_argument("-w", type=str, default="form", help="word file suffix")
PARSER.add_argument("-tr", type=str, default="tree", help="tree file suffix")
args = PARSER.parse_args()

# Python sucks at UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout) 
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

_DPBACKOFF = ""
_DPNGRAMS = set()
# model for DP_model
_DPMODEL = ""


def combine(a, b): return '%s.%s' % (a, b)

# Katz Backoff probability
def prob(prev, word, lemma, total, totalbi):
    uniprob = LEMMAS[lemma][word]/total
    if LEMMAS.has_key(combine(prev,lemma)):
        biprob = LEMMAS[combine(prev,lemma)][word]/totalbi
        if biprob > uniprob:
             return biprob
    return uniprob

def inflect(testing_prefix, total, totalbi):
    inflected = []
    for lemma_line, tree_line in izip(utf8read(combine(args.t, args.l)), utf8read(combine(args.t, args.tr))):
        l_sentence = lemma_line.rstrip().lower().split()
        tree = DepTree(tree_line)
        bgrams = dep_bigram(2, l_sentence, l_sentence, tree)
        forms = []
        prev = "<BOS>"
        for lemma, dep in izip(l_sentence, bgrams):
            if not LEMMAS.has_key(lemma):
                forms.append(lemma)
                continue
            best_form = None
            best_score = float('-inf')
            for form in LEMMAS[lemma]:
                score = prob(prev, form, lemma, total, totalbi)
                if score > best_score:
                        best_form = form
                        best_score = score
                forms.append(best_form)
                prev = lemma
                inflected.append(' '.join(forms))
    return inflected


def dep_bigram(n, l_sentence, f_sentence, tree):
    for lemma, form, node in izip(l_sentence, f_sentence, tree):
        # Try and get up to *n* nodes by traversing the tree.
        ngram = []
        current = node
        for i in xrange(n):
            if i == 0:
                ngram.insert(0, form)
            else:
                # Nodes are 1-indexed, so we have to subtract 1
                # to ensure that we've got the right word.
                ngram.insert(0, l_sentence[current.index() - 1])
            parent_index = node.parent_index()
            if parent_index == 0:
                break
            else:
                current = tree.node(parent_index)
        # Pad the *n*-gram to the right length.
        ngram = ('',) * (n - len(ngram)) + tuple(ngram)
        yield ngram
def lidstone(gamma):
     return lambda fd, bins: LidstoneProbDist(fd, gamma, bins)

def lidstone_estimator(fdist, bins):
    return LidstoneProbDist(fdist, 0.2)

def dependencybigram(n, lms, wds, trs):
    estimator = lidstone_estimator
    cfd = ConditionalFreqDist()
    for lm, wd, tr in izip(lms, wds, trs):
        for bgram in dep_bigram(n, lm, wd, tr):
            _DPNGRAMS.add(bgram)
            context = bgram[:-1]
            token = bgram[-1]
            cfd[context][token] += 1
    _DPMODEL = ConditionalProbDist(cfd, estimator, len(cfd))
    if n > 1:
        _DPBACKOFF = dependencybigram(n - 1, lms, wds, trs)

if __name__ == '__main__':

    # Build a simple unigram model on the training data
    #possible inflections for each lemma
    LEMMAS = defaultdict(defaultdict)
    total_lms = []
    total_wds = []
    total = 0
    totalbi = 0
    tree = []
    if args.t:
        def utf8read(file): return codecs.open(file, 'r', 'utf-8')
        # Build the LEMMAS hash, a two-level dictionary mapping lemmas to inflections to counts
        for words, lemmas, trees in izip(utf8read(combine(args.t, args.w)), utf8read(combine(args.t, args.l)), utf8read(combine(args.t, args.tr))):
            #for word1, lemma in izip(words.rstrip().lower().split(), lemmas.rstrip().lower().split()):
            prev = "<BOS>"
            word_dict = words.rstrip().lower().split()
            lemma_dict = lemmas.rstrip().lower().split()
            curr = []
            totalbi +=1
            for word, lemma in izip(word_dict, lemma_dict):
                total += 1
                LEMMAS[lemma][word] = LEMMAS[lemma].get(word,0) + 1
                LEMMAS[combine(prev,lemma)][word] = LEMMAS[combine(prev,lemma)].get(word,0) + 1
                prev = lemma
            total_lms.append(lemma_dict)
            total_wds.append(word_dict)
            tree.append(DepTree(trees))
        totalbi = total - totalbi
    dependencybigram(2, total_lms, total_wds, tree)

    # Choose the most common inflection for each word and output them as a sentence
    for line in sys.stdin:
        prev = "<BOS>"
        result = ""
        #words = line.rstrip().lower().split()
        for sentence in inflect(line.rstrip().lower().split(), total, totalbi):
            print sentence.encode('utf-8')
