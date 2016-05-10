#!/usr/bin/env python
import re
from collections import defaultdict
from itertools import izip
filename = "en-es-enwiktionary.txt"
dictionary = defaultdict(defaultdict)
for sentences in open(filename):
    es_words = []
    en_words  = sentences.split('::')[0]
    words = []
    try:
        if ',' in sentences.split('::')[1]:
            words = sentences.split('::')[1].rstrip('\n').rstrip(' ').strip(' ').strip('\t').split(',')
        else:
            words.append(sentences.split('::')[1].rstrip('\n').rstrip(' '))
    except:
        words.append(en_words)
    for word in words:
        if word not in es_words:
                    es_words.append(word.decode('utf-8'))
    if dictionary[en_words]== defaultdict(None,{}):
        dictionary[en_words] = es_words
    else:

        dictionary[en_words] += es_words
print dictionary["abandon"]
print dictionary["this"]
print dictionary["is"]
print dictionary["an"]
print dictionary["a"]
print dictionary["book"]
