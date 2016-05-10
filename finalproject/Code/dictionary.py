from collections import defaultdict
def create_dictionary():
    dictionary = defaultdict(defaultdict)
    for sentences in open("en-es-enwiktionary.txt"):
        es_words = []
        en_words  = sentences.split('::')[0]
        words = []
        try:
            if ',' in sentences.split('::')[1]:
                words = sentences.split('::')[1].rstrip('\n').rstrip(' ').strip(' ').strip('\t').split(',')
            else:
                words.append(sentences.split('::')[1].rstrip('\n').rstrip(' '))
        except:
            words.append(defaultdict(None,{}))
        for word in words:
            if word not in es_words:
                        es_words.append(word)
        if dictionary[en_words]== defaultdict(None,{}):
            dictionary[en_words] = es_words
        else:
            dictionary[en_words] += es_words
    return dictionary