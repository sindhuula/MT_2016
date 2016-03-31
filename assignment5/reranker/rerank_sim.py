import optparse
import bleu
import sys
import random

def compute_midpoint(p1, p2, wc, ut, mt):
  midpoint = {'p(e)': (p1['p(e)'] + p2['p(e)'])/2.0,
              'p(e|f)': (p1['p(e|f)'] + p2['p(e|f)'])/2.0,
              'p_lex(f|e)': (p1['p_lex(f|e)'] + p2['p_lex(f|e)'])/2.0,
              'word_count': wc,
              'untranslated_count':ut,
              'meteor':mt
             }
  return midpoint

def compute_reflection(pM, pW, wc, ut, mt):
  reflection = {'p(e)' : pM['p(e)'] + (pM['p(e)']-pW['p(e)']),
                'p(e|f)' : pM['p(e|f)'] + (pM['p(e|f)']-pW['p(e|f)']),
                'p_lex(f|e)' : pM['p_lex(f|e)'] + (pM['p_lex(f|e)']-pW['p_lex(f|e)']),
                'word_count': wc,
                'untranslated_count':ut,
                'meteor':mt
}
  return reflection

def compute_extension(pM, pW, wc, ut, mt):
  extension = {'p(e)' : pM['p(e)'] + 2.0*(pM['p(e)']-pW['p(e)']),
                'p(e|f)' : pM['p(e|f)'] + 2.0*(pM['p(e|f)']-pW['p(e|f)']),
                'p_lex(f|e)' : pM['p_lex(f|e)'] + 2.0*(pM['p_lex(f|e)']-pW['p_lex(f|e)']),
                'word_count': wc,
                'untranslated_count':ut,
                'meteor':mt
}
  return extension

def compute_bleu(hypothesis_list):
  ref = [line.strip().split() for line in open("data/dev.ref")]
  hyp = [hypothesis.strip().split() for hypothesis in hypothesis_list]

  stats = [0 for i in xrange(10)]
  for (r,h) in zip(ref, hyp):
    stats = [sum(scores) for scores in zip(stats, bleu.bleu_stats(h,r))]
  return bleu.bleu(stats)

optparser = optparse.OptionParser()
optparser.add_option("-k", "--kbest-list", dest="input", default="data/dev+test.100best.added.feats", help="100-best translation lists")
optparser.add_option("-l", "--lm", dest="lm", default=-1.0, type="float", help="Language model weight")
optparser.add_option("-t", "--tm1", dest="tm1", default=-0.5, type="float", help="Translation model p(e|f) weight")
optparser.add_option("-s", "--tm2", dest="tm2", default=-0.5, type="float", help="Lexical translation model p_lex(f|e) weight")
optparser.add_option("-w", "--wc", dest="wc", default=1.1, type="float", help="Word Count")
optparser.add_option("-u", "--ut", dest="ut", default=-1, type="float", help="Untranslated Words")
optparser.add_option("-m", "--mt", dest="mt", default=-1, type="float", help="Meteor Rate")
all_hyps = [pair.split(' ||| ') for pair in open(opts.input)]
num_sents = len(all_hyps) / 100
best_bleu = 0.0
actual_total = []

first_point = {'p(e)'       : float(random.randint(-1000, 1000)/1000),
               'p(e|f)'     : float(random.randint(-1000, 1000)/1000),
               'p_lex(f|e)' : float(random.randint(-1000, 1000)/1000),
               'word_count' : float(opts.wc)
               'untranslated_count':float(opts.ut)
               'meteor':float(opts.mt)
              }
second_point = {'p(e)'       : float(random.randint(-1000, 1000)/1000),
               'p(e|f)'     : float(random.randint(-1000, 1000)/1000),
               'p_lex(f|e)' : float(random.randint(-1000, 1000)/1000),
               'word_count' : float(opts.wc)
               'untranslated_count':float(opts.ut)
               'meteor':float(opts.mt)
              }
third_point = {'p(e)'       : float(random.randint(-1000, 1000)/100),
               'p(e|f)'     : float(random.randint(-1000, 1000)/100),
               'p_lex(f|e)' : float(random.randint(-1000, 1000)/100),
               'word_count' : float(opts.wc)
               'untranslated_count':float(opts.ut)
               'meteor':float(opts.mt)
              }

points = [first_point, second_point, third_point]

for i in range(10):
  bleu_scores = [] 
  for (n, p) in enumerate(points):
    total = []
    for s in xrange(0, num_sents):
      hyps_for_one_sent = all_hyps[s * 100:s * 100 + 100]
      (best_score, best) = (-1e300, '')
      for (num, hyp, feats) in hyps_for_one_sent:
        score = 0.0
        for feat in feats.split(' '):
          (k, v) = feat.split('=')
          score += p[k]*float(v)
        score += len(hyp.strip().split(' '))*p['word_count']
        
        # Check if there's russian characters. If so, reduce the score
        # because there's untranslated words
        for w in hyp.strip().split(' '):
          if ord(w[0]) >= 128 and ord(w[0]) <= 252: 
              score += -9.0
        
        if score > best_score:
          (best_score, best) = (score, hyp)
      total.append(best)
    bleu_scores.append((p, compute_bleu(total), total))

  best_point = sorted(bleu_scores, key = lambda x: -x[1])[0]
  good_point = sorted(bleu_scores, key = lambda x: -x[1])[1]
  worst_point = sorted(bleu_scores, key = lambda x: -x[1])[2]
  
  point_M = compute_midpoint(best_point[0], good_point[0], float(opts.wc), float(opts.ut),float(opts.mt))
  point_S = compute_midpoint(best_point[0], worst_point[0], float(opts.wc),float(opts.ut),float(opts.mt))
 
  # Slight confusion with naming: best_point is actually a tuple that includes
  # its bleu score
  points = [best_point[0], point_M, point_S]
  
  #this_bleu = compute_bleu(total)
  this_bleu = best_point[1]
  if this_bleu > best_bleu:
    best_bleu = this_bleu

sys.stderr.write(str(best_point[0])+ "\n")
for i in best_point[2]:
  try: 
    sys.stdout.write("%s\n" % i)
  except (Exception):
    sys.exit(1)

