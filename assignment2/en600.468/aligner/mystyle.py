#!/usr/bin/env python
import optparse
import sys
import math
from collections import defaultdict
#Input Parameters
optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
#Size of training data
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)
sys.stderr.write("Training with IBM Model 1...")
#Splits the files so that you get f[i] count, e[j] count and count(f,e)
#IBM stuff
#Find Prec, Rec and AER.
# Learn/Train: Expected Maximization for IBM Model 1
# EM Step
fprobs = {} #prob(f|e)
thetak_prob = {} #Theta prob
countfe = {} #Counter
counte = {} #coutner
n = 0
jump_counts = {}

def jump_key(j1, j0):
  return jump_counts.get(math.fabs(j1 - j0), 0)

def get_jump_transition(current_state, prev_state, L):
    s = jump_key(current_state, prev_state)
    j = [jump_key(l, prev_state) for l in range(L)]
    if sum(j) == 0:
        return 0.0
    else:
        return float(s) / float(sum(j))

for fsentence, esentence in zip(open(f_data),open(e_data)):
  if n % 500 == 0:
    sys.stderr.write("%s" %n)
  n = n + 1
  for fword in fsentence.rstrip(' .\n').split(' '):
    if fword not in fprobs:
      fprobs[fword] = {}
    total_sum = 0
    eprobs = {}
    e_pos = 0;
    for eword in esentence.rstrip(' .\n').split(' '):
      e_pos += 1
      if eword not in eprobs:
        eprobs[eword] = float(1)/float((len(esentence.rstrip(' .\n').split(' '))))
      else:
        eprobs[eword] += float(1)/float((len(esentence.rstrip(' .\n').split(' '))))
      if eword not in (fprobs[fword]):
        fprobs[fword][eword] = eprobs[eword]
      else:
        fprobs[fword][eword] += eprobs[eword]
      total_sum += fprobs[fword][eword]
    for eword in esentence.rstrip(' .\n').split(' '):
      hmm = get_jump_transition(e_pos, e_pos-1, (len(esentence.rstrip(' .\n').split(' '))))
      if hmm == 0.0:
        c = fprobs[fword][eword]
      else:
        c = fprobs[fword][eword]* hmm
      if (fword,eword) in countfe:
        countfe[(fword,eword)] += c
      else:
        countfe[(fword,eword)] = c
      if eword in counte:
        counte[eword] += c
      else:
        counte[eword] = c  
  for (fword, eword) in countfe:
    thetak_prob[(fword, eword)] = countfe[(fword, eword)]/counte[eword]

# Predict/Align: Most Probable Alignment:
# Alignment Step
n = 0
for fsentence, esentence in zip(open(f_data),open(e_data))[:opts.num_sents]:
  if n % 500 == 0:
    sys.stderr.write("%s?" %n)
  fnum = 0
  for fword in fsentence.rstrip(' .\n').split(' '):
      fnum = fnum + 1
      best_j =''
      best_prob = 0
      enum = 0
      for eword in esentence.rstrip(' .\n').split(' '):
       enum = enum + 1
       if thetak_prob[(fword, eword)] > best_prob:
          best_prob = thetak_prob[(fword, eword)]
          best_j = enum
      sys.stdout.write("%i-%i " % (fnum,best_j))
  sys.stdout.write("\n")
  n +=1