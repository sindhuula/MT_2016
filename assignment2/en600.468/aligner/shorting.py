#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict
with open('data/hansards.f') as f:
    n = 0
    while n < 1000:
        lines = f.readlines()
        with open("fren.f", "w") as f1:
            f1.writelines(lines)
        n = n+1
