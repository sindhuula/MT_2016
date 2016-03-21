#!/usr/bin/env python
from __future__ import division
from nltk.corpus import wordnet
synlist = []
for synset in wordnet.synsets('small'):
        for syn in synset.lemma_names():
            if syn.encode('ascii') not in synlist:
                synlist.append(syn.encode('ascii'))
print synlist
