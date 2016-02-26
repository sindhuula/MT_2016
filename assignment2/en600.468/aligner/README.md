Sarika Halarnakar - shalarn1
Sindhuula Selvaraju - sselvar4
Machine Translation Assignment 2: Word Alignment
2.25.16

Part 1: IBM Model 1

Usage: (In Aligner)
python align_IBM -n 1000 > ibm.a
python score-alignments < ibm.a 


Part 2: HMM + some experimentation

Usage: (In Aligner)
python align_HMM -n 1000 > hmm.a
python score-alignments < hmm.a 

Mathematical Desciption:

We decided to implement the HMM Alignment Model(It is our version of created by tweaking the IBM Model 1 that was designed). In an HMM Alignment, we assume that there is typically a strong localization effect in aliging the words in parallel text. That is, alignments have a strong tendency to remain in the local neighborhood of its source when translated into another language.

To implement an HMM model, we introduced a mapping of j -> i which assigns a french word in position j to an english word in position i.
The mathematical model captures the strong dependence of a_j on the previous alignement, thus the probability of alignment i for position j has a dependence on the previous alignment i' and the length of the english sentence:
		P(i| i', I)

There are three python programs here (`-h` for usage):

-`./align` aligns words.

-`./check-alignments` checks that the entire dataset is aligned, and
  that there are no out-of-bounds alignment points.

-`./score-alignments` computes alignment error rate.

The commands work in a pipeline. For instance:

   > ./align -t 0.9 -n 1000 | ./check | ./grade -n 5

The `data` directory contains a fragment of the Canadian Hansards,
aligned by Ulrich Germann:

-`hansards.e` is the English side.

-`hansards.f` is the French side.

-`hansards.a` is the alignment of the first 37 sentences. The 
  notation i-j means the word as position i of the French is 
  aligned to the word at position j of the English. Notation 
  i?j means they are probably aligned. Positions are 0-indexed.

We achieved the following statistics for 1000 sentence alignments:
Using IBM Model 1:

Using HMM Model:

Though the HMM model is not better than the IBM model this may be due to the fact the the jump_key being calculated is incorrect with respect to the language i.e. the words may have been reordered differently than calculated. Also, since we experimented with our attempt at creating an HMM model by changing different parameters the best one suited to our data may not have been found by us.