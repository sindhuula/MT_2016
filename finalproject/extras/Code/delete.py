#!/usr/local/bin/python
#coding=utf-8
from difflib import SequenceMatcher
import sys
from nltk import pos_tag, word_tokenize
reload(sys)
sys.setdefaultencoding('utf8')
text = word_tokenize("You know from the press and the television that there have been a series of explosions and killings in Sri Lanka .")
check1 = pos_tag(text)
check2 = pos_tag(word_tokenize("Sabrá usted por la prensa y la televisión que se han producido una serie de explosiones y asesinatos en Sri Lanka ."))
check3 = pos_tag(word_tokenize("sabrá usted por la prensa y la televisión que una serie de explosiones y asesinatos se en sri lanka ."))
print check1
print check2
print check3