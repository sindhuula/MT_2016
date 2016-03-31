# Add count of untranslated words and  to every line in test data
from __future__ import division
import optparse
import unicodedata

def meteor(h,e,a):
    precision,recall = findPrecisionRecall(h,e)
    try:
        l = (precision*recall) / (((1-a)*recall) + a*precision)
    except ZeroDivisionError:
        l = 0
    return (l)

def findPrecisionRecall(h,e):
    countcommon = 0
    sizeh = len(h)
    sizee = len(e)
    for word in h:
        if word in e:
            countcommon += 1
    recall = countcommon/sizee
    precision = countcommon/sizeh
    return (precision,recall)

if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-k", "--kbest-list", dest="input", default="data/dev+test.100best", help="100-best translation lists")
    optparser.add_option("-s", "--reference", dest="ref", default="data/dev.ref", help="Reference sentences")
    (opts, _) = optparser.parse_args()
    all_refs = [src.strip() for src in open(opts.ref)]
    all_hyps = [pair.split(' ||| ') for pair in open(opts.input)]

    writer = open(str(opts.input) + '.added.feats', 'w')
    for s in xrange(0, len(all_refs)):
        hyps_for_one_sent = all_hyps[s * 100:s * 100 + 100]
        for (num, hyp, feats) in hyps_for_one_sent:
            hyp_tokens = hyp.split()
            hyp_types = set(hyp_tokens)
            hyp_len = len(hyp_tokens)
            untranslated_count = 0

            for word in hyp_tokens:
            	flag = 0
            	for char in word:
            		if ord(char) >= 128 and ord(char) <= 252:
            			untranslated_count += 1
            			break;

      		ref = all_refs[s]
      		h1_match = meteor(hyp,ref,0.1)

            wc = ' ' + 'wc=' + str(hyp_len)
            utf = ' ' + 'ut=' + str(untranslated_count)
            mt = ' ' + 'mt=' + str(h1_match)
            new_feats = feats.strip() + wc + utf + mt
            new_line = num + ' ||| ' + hyp.strip() + ' ||| ' + new_feats.strip() + '\n'
            writer.write(new_line)

    writer.flush()
    writer.close()
    print
