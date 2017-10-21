In this assignment, you will implement a text classification system for sentiment analysis.  I will provide training data in the form of positive and negative hotel reviews.   Use this training data to develop a system that takes reviews as test cases and categorizes them as positive or negative.

Training data
The training data for this task consists of a collection of short hotel reviews. The data is formatted as one review per line. Each line starts with a unique identifier for the review (as in ID-2001) followed by tab and the text of the review.  The reviews are not tokenized or sentence segmented in any way (the words are space separated). The positive reviews and negative reviews appear in separate files.  You can assume that the training data is balanced with respect to class.

Here are two examples

ID-1274 Absolutely a great hotel for families! The rooms are spacious, restaraunts are very kid-friendly, and the pool area is gorgeous. My children felt like they were at a water park, not just another hotel. We will definitely return for another stay here!

ID-1021 This hotel is located at a busy traffic circle near the interstate. It isn't walking distance to downtown. The hotel restaurant was average. My wife complained about the quality of the sheets; they were pretty rough.
Testing
The test set will consist of a single file with mixed positive and negative reviews. As with training, you can assume the test set is balanced.

System Output
As output, your system should emit the review identifier followed by a tab and either a "POS" or "NEG" one per line for each review in the data.  As in:

ID-2838 POS
ID-2866 POS
ID-2858 NEG
ID-1186 NEG
ID-2904 POS
Approach
The easiest way to approach this problem is to use the naive Bayes approach that we went over in class (Chapter 6, Figure 6.3 to be exact).  Recall that this means building a unigram language model for each class and then assessing the probability of each test case with respect to each of the two models, with the highest probability class being the correct choice.  Correctly implementing naive Bayes along these lines is sufficient to get full credit for this assignment. To be specific, naive Bayes with add-1 smoothing will be the baseline used to assess performance.

Of course, naive Bayes isn't the best way to approach this problem. There are better approaches out there that you are free to use or implement.  For this assignment, you are free to use libraries like scikit-learn, nltk, or keras if you want to get fancy and go beyond naive Bayes. Note, this doesn't mean you can just submit some solution from the web that you find that uses one of these libraries.

Submissions
Submit the following:

A report detailing your approach, including a description of any libraries that you have chosen to use: lastname-firstname-assgn3-report.pdf

Your python code. If you have multiple files zip them together and include a README: lastname-firstname-assgn3.py

The output file for the provided test data: lastname-firstname-assgn3-out.txt