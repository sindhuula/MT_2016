#!/usr/bin/env python
import optparse
import sys
import models
from collections import namedtuple

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/input", help="File containing sentences to translate (default=data/input)")
optparser.add_option("-t", "--translation-model", dest="tm", default="data/tm", help="File containing translation model (default=data/tm)")
optparser.add_option("-l", "--language-model", dest="lm", default="data/lm", help="File containing ARPA-format language model (default=data/lm)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to decode (default=no limit)")
optparser.add_option("-k", "--translations-per-phrase", dest="k", default=20, type="int", help="Limit on number of translations to consider per phrase (default=1)")
optparser.add_option("-s", "--stack-size", dest="s", default=100, type="int", help="Maximum stack size (default=1)")
optparser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,  help="Verbose mode (default=off)")

opts = optparser.parse_args()[0]
tm = models.TM(opts.tm, opts.k)
lm = models.LM(opts.lm)
french = [tuple(line.strip().split()) for line in open(opts.input).readlines()[:opts.num_sents]]

#parameters
stepsize = 2.0
eta = -1.5
alpha_decrease_rate = 0.9
epsilon = 0.02
iteration_limit = 10
Constraints_limit = 2

# tm should translate unknown words as-is with probability 1
for word in set(sum(french,())):
  if (word,) not in tm:
    tm[(word,)] = [models.phrase(word, 0.0)]

sys.stderr.write("Decoding %s...\n" % (opts.input,))

def beam(f, u, Constraints):
  # The following code implements a monotone decoding
  # algorithm (one that doesn't permute the target phrases).
  # Hence all hypotheses in stacks[i] represent translations of 
  # the first i words of the input sentence. You should generalize
  # this so that they can represent translations of *any* i words.
  french_count = 0
  
  def distortion(end, newstart):
    return eta * abs(end + 1 - newstart)

  hypothesis = namedtuple("hypothesis", "logprob, LR_state, predecessor, phrase, y")
  LR_state = namedtuple("LR_state", "l, m, r, lm_state, bitstring")
  
  initial_y = [0 for i in range(len(f))]
  initial_bitstring = 0
  initial_lrstate = LR_state(0, 0, -1, lm.begin(), initial_bitstring)
  initial_hypothesis = hypothesis(0.0, initial_lrstate, None, None, initial_y)
  stacks = [{} for _ in f] + [{}]
  stacks[0][initial_lrstate] = initial_hypothesis
  
  for i, stack in enumerate(stacks[:-1]):
    for h in sorted(stack.itervalues(),key=lambda h: -h.logprob)[:opts.s]: # prune
      for k in xrange(0, len(f)):
        for j in xrange(i+1, len(f) + 1):
          if i + j - k > len(f):
            break
          if f[k:j] in tm:     
            #Update y vector
            new_y = h.y[:]
            for tmp in range(k, j):
              new_y[tmp] += 1
            #Compute the change of u[i] * y[i]            
            violation_change = sum(u[k: j])      
            if distortion(h.LR_state.r, k) > 6:
              continue
            for phrase in tm[f[k:j]]:
              current_lrstate = h.LR_state
              lm_state = current_lrstate.lm_state            
              logprob = h.logprob + phrase.logprob + violation_change + distortion(h.LR_state.r, k)
              #Prune using constraint set, or update new constraint set
              new_bitstring = current_lrstate.bitstring
              flag = False
              for (index, value) in enumerate(Constraints):
                if k<=value and value<j:
                  if (new_bitstring >> index) & 1 == 1:
                    flag = True
                  else:
                    new_bitstring = new_bitstring | (1 << index)
              if flag:
                continue
              for word in phrase.english.split():
                (lm_state, word_logprob) = lm.score(lm_state, word)
                logprob += word_logprob
              if k == current_lrstate.m+1:
                l = current_lrstate.l
                m = j -1
              else:
                if j == current_lrstate.l:
                  l = k
                  m = current_lrstate.m
                else:
                  l = k
                  m = j -1
              new_n = i + j - k
              r = j - 1
              new_lrstate = LR_state(l, m, r, lm_state, new_bitstring)
              if new_n == len(f):
                logprob += lm.end(lm_state)
              new_hypothesis = hypothesis(logprob, new_lrstate, h, phrase, new_y)
              if new_lrstate not in stacks[new_n] or stacks[new_n][new_lrstate].logprob < logprob: # second case is recombination
                stacks[new_n][new_lrstate] = new_hypothesis

          for l in xrange(i+1, k):
            #split phrase [i:l] [l:j]
            if f[k:l] in tm and f[l:j] in tm:
              #check each phrase the same way as above
              for phrase1 in tm[f[k:l]]:
                # phrase 2 same way as above
                #try:
                  for phrase2 in tm[f[l:j]]:
                    current_lrstate1 = h.LR_state
                    lm_state1 = current_lrstate.lm_state            
                    logprob1 = h.logprob + phrase2.logprob + violation_change + distortion(h.LR_state.r, j)
                    #Prune using constraint set, or update new constraint set
                    new_bitstring1= current_lrstate1.bitstring
                    flag1 = False
                    for (index, value) in enumerate(Constraints):
                      if k<=value and value<j:
                        if (new_bitstring1 >> index) & 1 == 1:
                          flag1 = True
                        else:
                          new_bitstring1 = new_bitstring1 | (1 << index)
                    if flag1:
                      continue
                    for word in phrase2.english.split():
                      (lm_state1, word_logprob1) = lm.score(lm_state1, word)
                      logprob1 += word_logprob1
                    if j == current_lrstate1.m+1:
                      l = current_lrstate1.l
                      m = j -1
                    else:
                      if l == current_lrstate1.l:
                        l1 = l
                        m = current_lrstate1.m
                      else:
                        l1 = l
                        m = j -1
                    new_n = i + j - l
                    r = j - 1
                    new_lrstate1 = LR_state(l1, m, r, lm_state1, new_bitstring1)
                    if new_n == len(f):
                      logprob1 += lm.end(lm_state1)
                    new_hypothesis1 = hypothesis(logprob1, new_lrstate1, h, phrase2, new_y)


                    current_lrstate2 = h.LR_state
                    lm_state2 = current_lrstate2.lm_state            
                    logprob2 = logprob1 + h.logprob + phrase1.logprob + violation_change + distortion(h.LR_state.r, k)
                    #Prune using constraint set, or update new constraint set
                    new_bitstring2= current_lrstate2.bitstring
                    flag2 = False
                    for (index, value) in enumerate(Constraints):
                      if k<=value and value<l:
                        if (new_bitstring2 >> index) & 1 == 1:
                          flag2 = True
                        else:
                          new_bitstring2 = new_bitstring2 | (1 << index)
                    if flag2:
                      continue
                    for word in phrase1.english.split():
                      (lm_state2, word_logprob2) = lm.score(lm_state2, word)
                      logprob2 += word_logprob2
                    if k == current_lrstate2.m+1:
                      l2 = current_lrstate2.l
                      m = l -1
                    else:
                      if l == current_lrstate2.l:
                        l2 = k
                        m = current_lrstate2.m
                      else:
                        l2 = k
                        m = l -1
                    new_n = i + l - k
                    r = l - 1
                    new_lrstate2 = LR_state(l2, m, r, lm_state2, new_bitstring2)
                    if new_n == len(f):
                      logprob2 += lm.end(lm_state2) if l == len(f) else 0.0
                    new_hypothesis2 = hypothesis(logprob2, new_lrstate2, new_hypothesis1, phrase1, new_y)
                    if new_lrstate2 not in stacks[j] or stacks[j][new_lrstate2].logprob < logprob2 and logprob1 < logprob2: # second case is recombination
                      stacks[j][new_lrstate2] = new_hypothesis2
                #except KeyError:
                 # continue



  winner = max(stacks[-1].itervalues(), key=lambda h: h.logprob)

  final_state = 1 << len(Constraints)
  def isOK(bitstring):
    return bitstring == final_state -1
  flag = False
  for h in sorted(stacks[-1].itervalues(),key=lambda h: -h.logprob)[:opts.s]: # prune
    if isOK(h.LR_state.bitstring):
      winner = h
      flag = True
      break

  def extract_english(h):
        return "" if h.predecessor is None else "%s%s " % (extract_english(h.predecessor), h.phrase.english)
  result = extract_english(winner)
  '''
  english_sentences = extract_english(winner)
  english_phrases = []
  current_winner = winner
  while current_winner[2] != None:
        current_phrase = current_winner[3].english
        english_phrases.append(current_phrase)
        current_winner = current_winner[2]
   
  english_phrases.reverse()
  total = 0.0
  for i in xrange(1, len(english_phrases) - 1):
        current = english_phrases[i]
        previous = english_phrases[i-1]
        if len(current.split()) > 1:
            current = current.split()[-1]
        next_phrase = english_phrases[i+1]
        if len(next_phrase.split()) > 1:
            next_phrase = next_phrase.split()[0]

        if (current, next_phrase) in lm.table and (previous, current) in lm.table:
            total += lm.table[(current, next_phrase)].logprob
        else:
            current = english_phrases[i+1]
            if len(current.split()) > 1:
                current = current.split()[-1]
            next_phrase = english_phrases[i]
            if len(next_phrase.split()) > 1:
                next_phrase = next_phrase.split()[0]

            if (current, next_phrase) in lm.table and (previous, current) in lm.table:
                total += lm.table[(current, next_phrase)].logprob
                english_phrases[i], english_phrases[i+1] = english_phrases[i+1], english_phrases[i]
  if total > winner.logprob:
        result = ' '.join(english_phrases)
  else:
        result = english_sentences

  if ' '.join(english_phrases).strip() != english_sentences.strip():
        french_count += 1
  '''
  ans = (winner, result)
  return ans

def optimize(f, u, Constraints):
  violation_count = [0 for i in range(len(f))]
  previous = -1e10
  lstar = (-1, -1e10)
  converged = False
  

  def isoptimal(y):
    for yi in y:
      if yi != 1:
        return False
    return True

  def update_count(y):
    for (i,yi) in enumerate(y):
      if yi != 1:
        violation_count[i] += 1
  now = 0
  step = stepsize
  while not converged:
    result = beam(f, u, Constraints)
    y = result[0].y
    if isoptimal(result[0].y):
      return result
    #check convergence
    if lstar[1] < result[0].logprob:
      if (result[0].logprob - lstar[1])/(now - lstar[0]) < epsilon:
        converged = True
      else:
        lstar = (now, result[0].logprob)
    #Update u
    for (i, yi) in enumerate(y):
      u[i] -= step * (yi - 1)
    #Update stepsize
    if result[0].logprob > previous:
      step = alpha_decrease_rate * step
    previous = result[0].logprob
    now += 1
    if (now - lstar[0] > iteration_limit):
      break
  K = iteration_limit
  G = Constraints_limit
  # Find the most violated element in y vector
  for iter_count in range(K):
    result = beam(f, u, Constraints)
    y = result[0].y
    #update count
    if isoptimal(y):
      return result
    update_count(y)

    #Update u
    for (i, yi) in enumerate(y):
      u[i] -= step * (yi - 1)
    #Update stepsize
    if result[0].logprob >previous:
      step = alpha_decrease_rate * step
    previous = result[0].logprob

  new_Constraints = Constraints[:]

  #Add G constraints
  for g in range(G):
    maxcount = -1
    maxindex = -1
    for (i, vi) in enumerate(violation_count):
      if (i-1) not in new_Constraints and i not in new_Constraints and (i+1) not in new_Constraints:
        if maxcount < vi:
          maxcount = vi
          maxindex = i
    new_Constraints.append(maxindex)
    new_Constraints.sort()
  return optimize(f, u, new_Constraints)
  
def main():
    for fsen in french:
      u = [0 for i in range(len(fsen))]
      result = optimize(fsen, u, [])
      print result[1]
if __name__ == '__main__':
  main()
