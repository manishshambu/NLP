In this assignment, you are to implement a learning based approach to named entity recognition.  In this approach, we can cast the problem of finding named entities as a sequence labeling task using IOB tags. One possible framework is to use the HMM-based solution developed for the POS tagging assignment.  The particular NER task we’ll be tackling is to find all the references to genes in a set of biomedical journal article abstracts. 

The training material consists of around 13000 sentences with gene references tagged with IOB tags.  Since we’re only dealing with one kind of entity here there are only three tag types in the data. The format of the data is identical to the POS tagging HW: one token per line associated with its proper tag (tab separated), sentences are separated with blank lines. An example is shown below. In this example there is one gene mentioned “human APEX gene” with the corresponding tag sequence B I I.

1 Structure O
2 , O
3 promoter O
4 analysis O
5 and O
6 chromosomal O
7 assignment O
8 of O
9 the O
10 human B
11 APEX I
12 gene I
13 . O
Although the structure of this problem is the same as POS tagging, the characteristics of the problem are quite different.  In particular, there are far fewer parameters to learn for transition probabilities since there are only three tags. However, the vocabulary is much larger than the BERP domain and unknown words will be far more prevalent.  The sentences are also much longer on average than the BERP examples. All of these considerations may lead you to different strategies from those you used in Assignment 2.

As with the last assignment, you're free to use any related machine learning approach or toolkit you like.  Your performance should however at least match that of an HMM approach.  You're also free to use external resources for training data. Just don't go looking around for this particular training set!

As noted in the book, evaluation of these kinds of systems is not based on per tag accuracy (you can do pretty well on that basis by just saying O all the time). What we really want to optimize is recall, precision and f-measures at the gene level.  Remember that precision is the ratio of correctly identified genes identified by the system to the total number of genes your system found,  and recall is the ratio of correctly identified genes to the total that you should have found.  The F1 measure given in the book is just the harmonic mean of these two.

I’ll use F1 to evaluate your systems on the withheld test data.  You should create a training and dev set from the data I’m providing for use in developing your system.  

As with the previous assignments, submit a report of what you did, your python code and test results.  I will post a test set before the due date.  Run the test data through your system and submit the output.  The output format of your system should be the same as the input training data: one token per line, with a tab separating the token from its tag, and a blank line separating sentences.
