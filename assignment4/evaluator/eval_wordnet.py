#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import nltk

def extract_key_words(text):
    # print text
    keywords = []
    # Used when tokenizing words
    sentence_re = r'''(?x)      # set flag to allow verbose regexps
          ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
        | \w+(-\w+)*            # words with optional internal hyphens
        | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
        | \.\.\.                # ellipsis
        | [][.,;"'?():-_`]      # these are separate tokens
    '''

    lemmatizer = nltk.WordNetLemmatizer()
    stemmer = nltk.stem.porter.PorterStemmer()

    #Taken from Su Nam Kim Paper...
    grammar = r"""
        NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
            
        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)

    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)

    #print postoks

    tree = chunker.parse(postoks)

    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')


    def leaves(tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            yield subtree.leaves()

    def normalise(word):
        """Normalises words to lowercase and stems and lemmatizes it."""
        word = word.lower()
        #word = stemmer.stem_word(word)
        word = lemmatizer.lemmatize(word)
        return word

    def acceptable_word(word):
        """Checks conditions for acceptable word: length, stopword."""
        accepted = bool(2 <= len(word) <= 40
            and word.lower() not in stopwords)
        return accepted


    def get_terms(tree):
        for leaf in leaves(tree):
            term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
            yield term

    terms = get_terms(tree)
    
    for term in terms:
        for word in term:
            keywords.append(word)
    return keywords
 
def word_matches(h, ref):
    return sum(1 for w in h if w in ref)
 
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
 
    count = 0
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        count += 1
        keywords_h1 = extract_key_words((' '.join(h1)).decode('utf-8'))
        keywords_h2 = extract_key_words((' '.join(h2)).decode('utf-8'))
        keywords_ref = extract_key_words((' '.join(ref)).decode('utf-8'))
        #rset = set(ref)
        #h1_match = word_matches(h1, rset)
        #h2_match = word_matches(h2, rset)
        #print(1 if h1_match > h2_match else # \begin{cases}
               # (0 if h1_match == h2_match
                #    else -1)) # \end{cases}
 
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
