#!/usr/bin/env python
import re
from collections import defaultdict
from itertools import izip
filename = "dictionary_es.rtf"
dictionary = defaultdict(defaultdict)
for sentences in izip(open("dictionary.rtf")):
#    print sentences[0]
    es_words = []
    en_words  = sentences[0].split('\\tab')[0]
    if ',' in sentences[0].split('\\tab')[1]:
        es_words.append(sentences[0].split('\\tab')[1].rstrip('\n').rstrip(' ').split(','))
    else:
        es_words.append(sentences[0].split('\\tab')[1].rstrip('\n').rstrip(' '))

    #print en_words,es_words
    dictionary[en_words] = es_words
print dictionary["this"]
print dictionary["is"]
print dictionary["a"]
print dictionary["book"]
