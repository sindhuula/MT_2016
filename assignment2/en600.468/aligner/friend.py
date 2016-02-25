#!/usr/bin/env python
import optparse
import subprocess
import operator
import sys
import pdb
import math
from subprocess import check_output
from collections import defaultdict


def sorte(t):
    return sorted(t.items(), key=operator.itemgetter(1))


def train(f_vocab, e_vocab, bitext):

    f_count = defaultdict(int)
    e_count = defaultdict(int)
    fe_count = defaultdict(int)
    total_e = defaultdict(float)
    s_total = defaultdict(float)
    t = defaultdict(float)
    # uniform probabilities
    for f_i in f_vocab:
        for e_j in e_vocab:
            t[(f_i, e_j)] = 1 / float(len(e_vocab))

    sys.stderr.write("Start...")

    for _ in range(5):
        for e_j in e_vocab:
            for f_i in f_vocab:
                fe_count[(f_i, e_j)] = 0
        for e_j in e_vocab:
            total_e[f_i] = 0

        for (n, (f, e)) in enumerate(bitext):
            # normalization
            for e_j in e:
                s_total[e_j] = 0
                for f_i in f:
                    s_total[e_j] += t[(f_i, e_j)]
            # collect counts
            for e_j in e:
                for f_i in f:
                    if s_total[e_j] == 0:
                        pdb.set_trace()
                    fe_count[(f_i, e_j)] += t[(f_i, e_j)] / float(s_total[e_j])
                    total_e[f_i] += t[(f_i, e_j)] / float(s_total[e_j])

        # estimate probabilities
        for f_i in f_vocab:
            for e_j in e_vocab:
                t[(f_i, e_j)] = fe_count[(f_i, e_j)] / total_e[f_i]

    return t


def main():

    optparser = optparse.OptionParser()
    optparser.add_option("-d", "--data",
                         dest="train",
                         default="data/hansards",
                         help="Data filename prefix (default=data)")
    optparser.add_option("-e", "--english",
                         dest="english",
                         default="e",
                         help="Suffix of English filename (default=e)")
    optparser.add_option("-f", "--french",
                         dest="french",
                         default="f",
                         help="Suffix of French filename (default=f)")
    optparser.add_option("-n", "--num_sentences",
                         dest="num_sents",
                         default=sys.maxint, type="int",
                         help="Number of sentences to use")
    (opts, _) = optparser.parse_args()
    f_data = "%s.%s" % (opts.train, opts.french)
    e_data = "%s.%s" % (opts.train, opts.english)

    sys.stderr.write("Training with IMB Modle 1...")
    bitext = [
            [sentence.strip().split() for sentence in pair]
            for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
    f_count = defaultdict(int)
    e_count = defaultdict(int)
    fe_count = defaultdict(int)
    total_e = defaultdict(float)
    s_total = defaultdict(float)
    t = defaultdict(float)
    f_vocab = set()
    e_vocab = set()

    f_length, e_length = 0, 0
    for x in range(opts.num_sents):
        sent = [sent for sent in bitext[x]]
        f_vocab.update(set(sent[0]))
        e_vocab.update(set(sent[1]))
    t = train(f_vocab, e_vocab, bitext)

    for (f, e) in bitext:
        for (i, f_i) in enumerate(f):
            best = [[], '', 0.0]
            for (j, e_j) in enumerate(e):
                if t[(f_i, e_j)] > best[2]:
                    best[2] = t[(f_i, e_j)]
                    best[1] = e_j
                    best[0] = [j]
                elif t[(f_i, e_j)] == best[2]:
                    best[0].append(j)
            found = False
            diffs = best[0]
            for x in range(len(diffs)):
                if math.fabs(diffs[x] - i) < 4:
                    sys.stdout.write("%i-%i " % (i, diffs[x]))
        sys.stdout.write("\n")


if __name__ == '__main__':
    main()
