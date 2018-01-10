# coding: utf-8

import nltk
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

class SentimentAnalyzer():
    def __init__ (self):
        self.positive_unigram_counts = dict()
        self.positive_unigram_prob = dict()
        self.negative_unigram_counts = dict()
        self.negative_unigram_prob = dict()
        self.positive_sent_ids = list()
        self.negative_sent_ids = list()
        self.positive_word_list = list()
        self.negative_word_list = list()
        self.positive_sent_list = list()
        self.negative_sent_list = list()
        self.all_sent_list = list()
        self.test_sent_list = list()
        self.all_label_list = list()
        self.all_word_list = list()
        self.sent_id_list = list()
        self.all_word_prob = dict()
        self.positive_sent_len = 0
        self.negative_sent_len = 0
        self.positive_prior = 0
        self.negative_prior = 0
        self.vectorizer = None
        self.stop_words_puncts = ['the', 'a', '.', '!', '?', 'an', 'with', 'without', 'I', 'wife', ':', ',', 'can', 'Can', 'How', 'how', '\\', '\'', '\"', '(', ')']
        #self.stop_words_puncts = []

    def setUpVocab (self, positive_doc, negative_doc):
        fp = open(positive_doc, "r")
        lines = fp.readlines()
        self.positive_sent_len = len(lines)

        for line in lines:
            l = line.strip("\n")
            #self.all_sent_list.append(l)
            #self.all_label_list.append("T")
            words = line.split()
            space =  " "
            sentence = space.join(words[1:])
            self.all_sent_list.append(sentence.strip("\n"))
            self.all_label_list.append("T")
            toks = nltk.word_tokenize(sentence)
            toks_without_stop = list()
            for t in toks:
                if t in self.stop_words_puncts:
                    continue
                else:
                    toks_without_stop.append(t)

            self.positive_word_list.extend(toks_without_stop)
            self.positive_sent_ids.append(words[0])
        
        fp.close()
        fp = open(negative_doc, "r")
        lines = fp.readlines()
        self.negative_sent_len = len(lines)

        for line in lines:
            l = line.strip("\n")
            #self.all_sent_list.append(l)
            #self.all_label_list.append("F")
            words = line.split()
            if len(words) == 0:
                continue
            space =  " "
            sentence = space.join(words[1:])
            self.all_sent_list.append(sentence.strip("\n"))
            self.all_label_list.append("F")
            toks = nltk.word_tokenize(sentence)
            toks_without_stop = list()
            for t in toks:
                if t in self.stop_words_puncts:
                    continue
                else:
                    toks_without_stop.append(t)
            self.negative_word_list.extend(toks_without_stop)
            self.negative_sent_ids.append(words[0])
            #print words[0], "--->", toks

        self.all_word_list = set(self.negative_word_list + self.positive_word_list) 
        #print len(self.all_word_list)
        self.positive_prior = math.log((self.positive_sent_len * 1.0)/(self.positive_sent_len + self.negative_sent_len))
        self.negative_prior = math.log((self.negative_sent_len * 1.0)/(self.positive_sent_len + self.negative_sent_len))

        fp.close()
  
    def populateAllWordUnigrams (self):
        for w in self.all_word_list:
            self.all_word_prob[w] = dict()

        for w in self.all_word_list:
            if w not in self.positive_word_list:
                count_w = 0
            else:
                count_w = self.positive_unigram_counts[w]

            self.all_word_prob[w]["pos"] = math.log((1.0 * (count_w+1))/(len(self.positive_word_list) + len(self.all_word_list)))
        
            if w not in self.negative_word_list:
                count_w = 0
            else:
                count_w = self.negative_unigram_counts[w]

            self.all_word_prob[w]["neg"] = math.log((1.0 * (count_w+1))/(len(self.negative_word_list) + len(self.all_word_list)))

    def populatePositiveUnigrams (self):
        for pos_word in self.positive_word_list:
            if pos_word not in self.positive_unigram_counts:
                self.positive_unigram_counts[pos_word] = 1
            else:
                self.positive_unigram_counts[pos_word] += 1
        '''
        for pos_word in self.positive_word_list:
            self.positive_unigram_prob[pos_word] = 1.0 * (self.positive_unigram_counts[pos_word] + 1)/(len(self.positive_word_list) + len(self.all_word_list)) 
        '''

    def populateNegativeUnigrams (self):
        for neg_word in self.negative_word_list:
            if neg_word not in self.negative_unigram_counts:
                self.negative_unigram_counts[neg_word] = 1
            else:
                self.negative_unigram_counts[neg_word] += 1
        '''
        for neg_word in self.negative_word_list:
            self.negative_unigram_prob[neg_word] = 1.0 * (self.negative_unigram_counts[neg_word] + 1)/(len(self.negative_word_list) + len(self.all_word_list)) 
        '''

    def printValues(self):
        print len(self.positive_word_list)
        print len(self.negative_word_list)
        print len(self.all_word_list)
        print "ALL WORD LIST COMING UP"
        print self.all_word_list
        print self.positive_sent_len
        print self.negative_sent_len
        print self.positive_prior
        print self.negative_prior
        
        '''
        print "==========POSITIVE PROB====================="
        print self.positive_unigram_prob
        print "==========POSITIVE COUNT===================="
        print self.positive_unigram_counts
        print "==========NEGATIVE PROB====================="
        print self.negative_unigram_prob
        print "==========NEGATIVE COUNT===================="
        print self.negative_unigram_counts
        '''

    def naiveBayesTest(self, tes_file, out_file):
        fp = open(tes_file, "r")
        lines = fp.readlines()
        space = " "
        output_string = ""
        for line in lines:
            l = line.strip("\n")
            self.test_sent_list.append(l) 
            words = line.split()
            word_l = words[1:]
            sent = space.join(word_l)
            sent_id = words[0]
            sent_output = self.classifySentence(sent)
            output_string += (sent_id + "\t" + sent_output + "\n")

        fp.close()

        fp = open(out_file, "w")
        fp.write(output_string)
        fp.close()

    def svmTest (self, tes_file, out_file):
        fp = open(tes_file, "r")
        lines = fp.readlines()
        space = " "
        output_string = ""
        for line in lines:
            words = line.split()
            word_l = words[1:]
            sent = space.join(word_l)
            self.test_sent_list.append(sent) 
            self.sent_id_list.append(words[0])

        fp.close()
       
        res = self.trainSVM()
        out_str = ""

        print len(res)
        print len(self.sent_id_list)

        for s in range(0,len(self.sent_id_list)):
            out_str += (self.sent_id_list[s] + "\t" + res[s] + "\n")

        fp = open(out_file, "w")
        fp.write(out_str)
        fp.close()


    def trainSVM(self):
        self.vectorizer = TfidfVectorizer (min_df=5,
                                           max_df=0.8,
                                           sublinear_tf=True,
                                           use_idf=True)

        cv = CountVectorizer()

        train_vectors = self.vectorizer.fit_transform(self.all_sent_list)
        #sent_vector = cv.fit_transform (self.sent_list)
        test_vectors = self.vectorizer.transform(self.test_sent_list)
       

        classifier = svm.SVC(kernel='linear')
        classifier.fit(train_vectors, self.all_label_list)
        prediction = classifier.predict(test_vectors)
        return prediction

    def classifySentence (self, test_sent):
        words = nltk.word_tokenize(test_sent)
        sent_id = words[0]
        words = words[1:]
        pos_prob = self.positive_prior
        neg_prob = self.negative_prior

        for w in words:
            if w not in self.all_word_list:
                neg_prob_val = 0
                pos_prob_val = 0
            else:
                pos_prob_val = self.all_word_prob[w]["pos"]
                neg_prob_val = self.all_word_prob[w]["neg"]
            
            pos_prob += pos_prob_val
            neg_prob += neg_prob_val

        #print "NEG PROB --- >" , str(neg_prob) 
        #print "POS PROB --- >" , str(pos_prob) 

        if neg_prob > pos_prob:
            return "F"
        else:
            return "T"

sentAnalyzer = SentimentAnalyzer()
#sentAnalyzer.setUpVocab ("hotelPosT-train.txt", "hotelNegT-train.txt")
sentAnalyzer.setUpVocab ("hotelT-train.txt", "hotelF-train.txt")
sentAnalyzer.populatePositiveUnigrams()
sentAnalyzer.populateNegativeUnigrams()
sentAnalyzer.populateAllWordUnigrams()
#sentAnalyzer.naiveBayesTest ("hotelTest.txt", "hotelTestOutput.txt");
#sentAnalyzer.naiveBayesTest ("devtest.txt", "martinTestOutput.txt");
sentAnalyzer.svmTest("devtest.txt", "martinTestOutput.txt")
#sentAnalyzer.printValues()
