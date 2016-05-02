#!/usr/bin/env python
from nltk.parse.malt import MaltParser
parser = MaltParser('maltparser-1.8.1','espmalt-1.0.mco')
txt="This is a test sentence"
parser.train_from_file('Tibidabo_Treebank.txt')
parser.raw_parse(txt)