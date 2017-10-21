# NLP
In this assignment, we'll explore the statistical approach to part-of-speech tagging.

Training data
We'll be using POS-tagged data from the Berkeley Restaurant corpus as our training data. There are around 15,000 sentences in this corpus.  You should assume that the POS tag set is closed (the tags in the training data are all there are).  On the other hand, you should assume that new words will occur in the test data. The sentences are arranged as one word per line with a blank line separating the sentences. The columns are tab separated, with the first column giving word position, the second the word and the third the POS tag. The following example illustrates this format.


Position	Word-form	Tag
1	i	PRP
2	'd	MD
3	like	VB
4	french	JJ
5	food	NN
6	.	.

Evaluation
To determine if you're making any progress, you'll need an evaluation script. I'm providing a very basic script that calculates overall accuracy compared to a gold standard evaluation set.  Call it as follows from a unix command line:

python eval-pos.py  gold-file system-file
A more useful tool would produce a confusion matrix.  You're welcome to implement such tool as part of your submission.


Probabilistic Tagger
Baseline

As a baseline system, you should first implement a "most frequent tag" system. Given counts from the training data, your tagger should simply assign to each input word the tag that it was most frequently assigned to in the training data.  This is a reasonable approach and will allow you to assess the performance of your more advanced approach.

Viterbi

Once you have a working baseline, implement the Viterbi algorithm with a bigram-based approach. Specifically, you'll need to:

Extract the required counts from the training data to generate the required probability estimates for the model.
Deal with unknown words in some sensible way.
Do some form of smoothing for the bigram tag model.
Implement a Viterbi decoder.
Evaluate your system's performance on unseen data.
At test time, your system should accept a file in the same format as the training date (without the final column of POS tags).   The output should be in the format (with the final column).  Remember the columns are tab separated. 

Deliverables
You will need to turn in your code, along with a short report describing what you did and all the choices you made. You should include in your report how you developed and assessed your system (training/dev) and how well you believe it should work on unseen test data. In addition, I will provide a test set for you to run your system on shortly before the due date.  Include the output of your system on this test data in the same form as the training data.
