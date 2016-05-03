#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import codecs

import sys
from itertools import izip

from PyDictionary import PyDictionary
dictionary = PyDictionary()
PARSER = argparse.ArgumentParser(description="Reorder a set of sentences")
PARSER.add_argument("-t", type=str, default="train", help="file to be translated prefix")
PARSER.add_argument("-es", type=str, default="es", help="spanish file")
PARSER.add_argument("-en", type=str, default="en", help="english file")
args = PARSER.parse_args()

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

def combine(a, b): return 'data/%s.%s' % (a, b)

if __name__ == '__main__':

    if args.t:
        def utf8read(file): return codecs.open(file, 'r', 'utf-8')
        for en_sentences,es_sentences in izip(utf8read(combine(args.t,args.en)),utf8read(combine(args.t,args.es))):
            print en_sentences
            new_sent = ""
            new_words = []
            for word in en_sentences.rstrip().lower().split():
                translation = []
                print word
                temp  = dictionary.translate(word,"es")


                if temp == None:
                    new_words.append(str(word))
                else:
                    translation.append(dictionary.synonym(temp))
                    if translation in es_sentences.rstrip().lower().split():
                        new_words.append(str(translation))
            new_sent = ' '.join(new_words)
            print new_sent



