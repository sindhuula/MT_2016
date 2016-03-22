#!/usr/bin/env python
from __future__ import division 
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
from nltk.corpus import wordnet
import nltk
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
def findSyn(sentence):
    print "findsyn"
    synlist = []
    print "sentence", sentence
    for word in sentence:
#     try:
        for synset in wordnet.synsets(word):
            for syn in synset.lemma_names():
                if syn.decode('utf8') not in synlist:
                    synlist.append(syn.decode('utf8'))
 #    except UnicodeDecodeError
        if word not in synlist:
            synlist.append(word)
    print "synlist",synlist
    return synlist
def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""

    word = word.lower()
    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word 

def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
            help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
            help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()
 
    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
 
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        rset = set(ref)
        print "rseta",rset
        h1_match = word_matches(h1, rset)
        print "rsetb",rset
        h2_match = word_matches(h2, rset)
        print "rsetc",rset
        result = (1 if h1_match > h2_match else # \begin{cases}
                (0 if h1_match == h2_match
                    else -1)) # \end{cases}
        with open('result1', 'a') as f:
            f.write("%s\n" % str(result))
    a = 0.1
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        rset = set(ref)
        print "rset1",rset
        h1_match = meteor(h1,rset,a) 
        print "rset2",rset
        h2_match = meteor(h2,rset,a)
        print "rset3",rset
        result = (1 if h1_match > h2_match else # \begin{cases}
                (0 if h1_match == h2_match
                    else -1)) # \end{cases}
        with open('result_synstem', 'a') as f:
            f.write("%s\n" % str(result))
            
def meteor(h,e,a):
    precision,recall = findPrecisionRecall(h,e)
    try:
        l = (precision*recall) / (((1-a)*recall) + a*precision)
    except ZeroDivisionError:
        l = -1
    return (l)

def findPrecisionRecall(h,e):
    print "find ",e
    countcommon = 0
    sizeh = len(h)
    sizee = len(e)
    synset = findSyn(e)
    synstem = []
    for word in synset:
        synstem.append(normalise(word.decode('utf8')))
#  for i in synstem:
 #       e.add(i)
    print synstem
    for word in h:
        if normalise(word.decode('utf8')) in synstem:
            countcommon += 1
    recall = countcommon/sizee
    precision = countcommon/sizeh
    return (precision,recall)
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
