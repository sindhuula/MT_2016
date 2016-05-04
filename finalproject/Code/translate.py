#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import codecs

import sys
from collections import defaultdict
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
    dictionary = defaultdict(defaultdict)
    for sentences in izip(open("dictionary.rtf")):
        es_words = []
        en_words  = sentences[0].split('\\tab')[0].lower()
        if ',' in sentences[0].split('\\tab')[1]:
         temp_words =(sentences[0].split('\\tab')[1].rstrip('\n').rstrip(' ').split(','))
         for word in temp_words:
                es_words.append(word)
        else:
              es_words.append(sentences[0].split('\\tab')[1].rstrip('\n').rstrip(' '))
        dictionary[en_words] = es_words
    if args.t:
#        translated_file = open("data/translate.es","w")
        def utf8read(file): return codecs.open(file, 'r', 'utf-8')
        for en_sentences,es_sentences in izip(utf8read(combine(args.t,args.en)),utf8read(combine(args.t,args.es))):
            new_sent = ""
            new_words = []
            for word in en_sentences.rstrip().lower().split():
                translation = []
                if dictionary[word] == defaultdict(None, {}):
                    new_words.append(str(word))
                else:
                    translation = dictionary[word]
                    for es_word in translation:
                        if es_word in es_sentences.rstrip().lower().split():
                            new_words.append(str(es_word))
            new_sent = ' '.join(new_words)
            print new_sent

 #           translated_file.write(new_sent)
#            translated_file.write("\n")
