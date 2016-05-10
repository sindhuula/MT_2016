#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import codecs
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem.lancaster import LancasterStemmer
import sys
from collections import defaultdict
from itertools import izip

from PyDictionary import PyDictionary
stemmer = LancasterStemmer()
lemmatizer = WordNetLemmatizer()
pydictionary = PyDictionary()
PARSER = argparse.ArgumentParser(description="Reorder a set of sentences")
PARSER.add_argument("-t", type=str, default="trial", help="file to be translated prefix")
PARSER.add_argument("-es", type=str, default="es", help="spanish file")
PARSER.add_argument("-en", type=str, default="en", help="english file")
args = PARSER.parse_args()

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

def combine(a, b): return 'data/%s.%s' % (a, b)
def append(current,dicts):
    for words in dicts:
        current.append(words)
    return current
def translate(en_sentences,es_sentences,dictionary):
            def utf8read(file): return codecs.open(file, 'r', 'utf-8')
            found = defaultdict(bool)
            es_no = 0
            new_sent = ""
            new_words = []
            found_es = defaultdict(bool)
            prev = "BOS"
            prev_prev = "BOS"
            for word in en_sentences.rstrip().lower().split():
                es_no+=1
                flag = False
                translation = []
                if(dictionary[prev_prev+" "+word]==defaultdict(None,{})):
                    if(dictionary[prev+" "+word] == defaultdict(None,{})):
                        if (dictionary[word] == defaultdict(None,{})):
                            if dictionary[lemmatizer.lemmatize(word)] == defaultdict(None, {}):
                             if dictionary[stemmer.stem(word)] == defaultdict(None,{}):
                                if(dictionary[prev+" "+word]) == defaultdict(None,{}):
                                    if(dictionary[prev_prev+" "+prev+" "+word]) == defaultdict(None,{}):
                                        translation = append(translation,[str(word)])
                                    else:
                                        translation = append(translation,dictionary[prev_prev+" "+prev+" "+word])
                                else:
                                        translation = append(translation,dictionary[prev+" "+word])
                             else:
                                translation = append(translation,dictionary[stemmer.stem(word)])

                            else:
                             translation = append(translation,dictionary[lemmatizer.lemmatize(word)])
                        else:
                             translation = append(translation,dictionary[word])
                    else:
                        translation = append(translation,dictionary[prev+" "+word])
                else:
                    translation = append(translation,dictionary[prev_prev+" "+prev+" "+word])
                for es_word in translation:
                        word_no = 0
                        prev_sp = "BOS"
                        for spanish_word in es_sentences.rstrip().lower().split():
                              word_no+=1
                              if found_es[es_no] == False:
                                  if(es_word.decode('utf-8').lower() == spanish_word.decode("utf-8")):
                                          new_words.append(spanish_word)
                                          found[word_no] = True
                                          found_es[es_no] = True
                                          break
                                  elif (es_word.decode('utf-8').lower() == lemmatizer.lemmatize(spanish_word.decode("utf-8")))|(es_word.decode('utf-8').lower()==stemmer.stem(spanish_word.decode("utf-8"))):
                                          new_words.append(spanish_word)
                                          found[word_no] = True
                                          found_es[es_no] = True
                                          break
                                  elif es_word.decode('utf-8').lower() == prev_sp+" "+spanish_word.decode("utf-8"):
                                          new_words.append(spanish_word)
                                          found[word_no] = True
                                          found_es[es_no] = True
                                          break
                              prev_sp = spanish_word.decode("utf-8")

                prev_prev = prev
                prev = word
            new_sent = ' '.join(new_words)
            return new_sent