#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Outputs a version where the phrases are re-ordered in SVO order
TODO Change the order within the phrase and improve reordering
"""
import openpyxl
import argparse
import codecs
import sys
from collections import defaultdict
from itertools import izip, islice

PARSER = argparse.ArgumentParser(description="Reorder a set of sentences")
PARSER.add_argument("-t", type=str, default="data/train", help="training data prefix")
PARSER.add_argument("-d", type=str, default="data/dev", help="dev data prefix")
PARSER.add_argument("-w", type=str, default="es", help="spanish file")
PARSER.add_argument("-p", type=str, default="xlsx", help="tag file")
args = PARSER.parse_args()

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
def sentences():
        with open(combine(args.d,args.w)) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]

def combine(a, b): return '%s.%s' % (a, b)

def compare(hypothesis1,hypothesis2,reference):
    hyp1 = hypothesis1.rstrip.lower.strip()
    hyp2 = hypothesis2.rstrip.lower.strip()
    ref = reference.rstrip.lower.strip()
    length = len(ref)
    common_hyp1 = 0
    common_hyp2 = 0
    for i in range(length):
        if hyp1[i] == ref[i]:
            common_hyp1 += 1
        if hyp2[i] == ref[i]:
            common_hyp2 += 1
    if common_hyp1 > common_hyp2:
        return hypothesis1
    else:
        return hypothesis2

if __name__ == '__main__':

    if args.t:
        sentence_tags = defaultdict(list)
        def utf8read(file): return codecs.open(file, 'r', 'utf-8')
        #TODO: Do we really need training
        #Training Section
        #Incorrect_ordering = word, dep_tag pair
        #Correct ordering = word, dep_tag pair
        wb = openpyxl.load_workbook(args.p)
        parsed = wb.get_sheet_by_name(args.t)
        sentence_no = 0
        order = []
        sentences = defaultdict(defaultdict)
        properties = []
        rows = int( parsed.get_highest_row())
        columns = int(parsed.get_highest_column())
        print rows,columns
        for i in range(1, rows+1):
            if parsed.cell(column = 1, row = i).value == 1 :
                word_props = defaultdict(list)
                sentence_no +=1
                word_props[parsed.cell(column = 2, row = i).value] =  [parsed.cell(column = 4, row = i).value, parsed.cell(column = 5, row = i).value,parsed.cell(column = 8, row = i).value]
                sentences[sentence_no] = word_props

        #Dev Section
        wb = openpyxl.load_workbook(combine(args.d,args.p))
        parsed = wb.get_sheet_by_name('first_1000')
        sentence_no = 0
        order = []
        sentences = defaultdict(defaultdict)
        properties = []
        rows = int( parsed.get_highest_row())
        columns = int(parsed.get_highest_column())
        print rows,columns
        for i in range(1, rows+1):
            if parsed.cell(column = 1, row = i).value == 1 :
                word_props = defaultdict(list)
                sentence_no +=1
                word_props[parsed.cell(column = 2, row = i).value] =  [parsed.cell(column = 4, row = i).value, parsed.cell(column = 5, row = i).value,parsed.cell(column = 8, row = i).value]
                sentences[sentence_no] = word_props
        verb_phrase = ""
        subj_phrase = ""
        obj_phrase = ""
        noun_phrase = ""
        subjects = ["SUBJ"]
        objects = ["DO","IO","OBLC"]
        verbs = ["v"]
        sent_no = 0
        for hypothesis1, hypothesis2, original_sentence in islice(sentences()):
            sent_no += 1
            final_sent = ""
            temp_phrase = []
            words = sentences[sent_no]
            for word in words:
                if word != None:
                    if (type(word) == long) | (type(word) == float) | (type(word) == int):
                        word = unicode(str(word),"utf-8")
                    temp_phrase.append(word)

                if word[2] in subjects:
                    subj_phrase = ' '.join(temp_phrase)
                    temp_phrase = []
                elif word[2] in objects:
                    obj_phrase = ' '.join(temp_phrase)
                    temp_phrase = []
                elif word[0] in verbs:
                    verb_phrase = ' '.join(temp_phrase)
                    temp_phrase = []
            final_sent = subj_phrase+' '+verb_phrase+' '+obj_phrase
            print compare(hypothesis1,hypothesis2,final_sent)

            #hyp1 = h1
            #hyp2 = h2
            #ref = orig sent



        # From the trained portion find out how the tags were re-ordered and try to replicate
        # Our program simply just exchanges the phrases
        print "Read the sentences"
        print "Read the tag files for the sentences"
        print "Shuffle phrases"
        print "Train set may actually help to identify the correct ordering of the words and give an idea about how to reshuffle the tags"
        print "Dev and test set need to use the training model to see how to get an output"

