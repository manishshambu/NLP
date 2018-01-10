In this assignment, you will implement a text classification system for deception detaction.  I will provide training data in the form of truthful and deceptive hotel reviews.   Use this training data to develop a system that takes reviews as test cases and categorizes them as one or the other. 

Training data
The training data for this task consists of a collection of short hotel reviews. All reviews were written about real hotels by people with first-hand experience with the hotels.  The truthful reviews are... truthful.  The deceptive reviews describe an experience opposed to what the writer actually experienced. The data is formatted the same as the earlier sentiment HW; one review per line. Each line starts with a unique identifier for the review (as in ID-2001) followed by tab and the text of the review.  The reviews are not tokenized or sentence segmented in any way (the words are space separated). The two classes of reviews appear in separate files.  You can assume that the training data is balanced with respect to class.

Testing

The test set will consist of a single file with mixed positive and negative reviews. As with training, you can assume the test set is balanced.

System Output
As output, your system should emit the review identifier followed by a tab and either a "T" or "F" one per line for each review in the data.  As in:

ID-2838 T
ID-2866 T
ID-2858 F
ID-1186 T
ID-2904 F
Approach
The easiest way to approach this problem is to use the naive Bayes approach that we went over in class. Sentiment is a particularly important aspect of this problem.  For this assignment, you are free to use libraries like scikit-learn, nltk, or keras if you want to get fancy and go beyond naive Bayes. Note, this doesn't mean you can just submit some solution from the web that you find that uses one of these libraries.

Submissions
Submit the following:

A report detailing your approach, including a description of any libraries that you have chosen to use: lastname-firstname-extra-report.pdf

Your python code. If you have multiple files zip them together and include a README: lastname-firstname-extra.py

The output file for the provided test data: lastname-firstname-extra-out.txt
