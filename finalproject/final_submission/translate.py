#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import codecs

import re
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
            translations = defaultdict(defaultdict)
            def utf8read(file): return codecs.open(file, 'r', 'utf-8')
            found = defaultdict(bool)
            new_words = []
            new_sent = ""
            prev = "BOS"
            prev_prev = "BOS"
            for word in en_sentences.rstrip().lower().split():
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
                        translations.pop(prev)
                        word = prev+" "+word
                else:
                    translation = append(translation,dictionary[prev_prev+" "+prev+" "+word])
                    translations.pop(prev_prev)
                    translations.pop(prev)
                    #translations.pop(prev_prev+" "+prev)
                    word = prev_prev+" "+prev+" "+word
                translations[word] = translation
                prev_prev = prev
                prev = word
            word_no = -1
            sent = en_sentences.rstrip().lower().split()
            for word in sent:
              word_no+=1
              try:
                  if (sent[word_no-1]+" "+sent[word_no-1]+" "+word) in translations.keys():
                      word = sent[word_no-1]+" "+sent[word_no-1]+" "+word
                  elif sent[word_no-1] +" "+ word in translations.keys():
                    word = sent[word_no-1]+" "+word
                  else:
                    word = word
              except:
                  word = word
              es_no = 0
              found_es = defaultdict(bool)
              for es_word in translations[word]:
                        word_no = 0
                        prev_sp = "BOS"
                        for spanish_word in es_sentences.rstrip().lower().split():
                              regex = re.compile('[,\.!?]')
                              spanish_word = regex.sub('', spanish_word)

                              word_no+=1
                              if found_es[es_no] == False:
                                  if(es_word == spanish_word):
                                          new_words.append(spanish_word)
                                          found[word_no] = True
                                          found_es[es_no] = True
                                          break

                                  elif es_word == prev_sp+" "+spanish_word:
                                          new_words.append(spanish_word)
                                          found[word_no] = True
                                          found_es[es_no] = True
                                          break
                              prev_sp = spanish_word
            new_sent = ' '.join(new_words)
            return new_sent