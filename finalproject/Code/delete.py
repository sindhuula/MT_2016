#!/usr/bin/env python
import re
from itertools import izip

regex = re.compile(".*?\((.*?)\)")
for sentences in izip(open("dictionary.rtf")):
    print sentences[0]
    