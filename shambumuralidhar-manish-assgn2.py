import re
import operator
import os.path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

most_frequent_tags = dict()
word_pos_tags = dict()
word_counts = dict()
word_counts_sorted = dict()
InputFileName = "berp-POS-training-small.txt"
testFileName = "berp-POS-test.txt"
testFileName = "berp-POS-test.txt"
dir_path = ""
trainingFile = "training.txt"
testExpectedFile = "test_expected.txt"
testFile = "test.txt"

prefix_pattern = "(^[0-9])"

def arrangeSentencesInEachLine(trainingInputContent):
    if prefix_pattern:
        sentenceArray = []
        newline = ""
        for line in trainingInputContent:
            m = re.search(prefix_pattern, line)
            if m:
                newline = newline + line.strip() + ","
            else:
                sentenceArray.append(newline.strip(","))
                sentenceArray.append("\n")
                newline = ""
        return sentenceArray
    else:
        return trainingInputContent


'''
Build the base line model. Read each line from the file.
Split the line based on tab. Extract the word name and matching POS.
Create a dict(dicts[count]):
1. Key for outer dict is the word name
2. Key for inner dict is the matching POS
3. Value for inner dict is the count for each POS

Create a new dict with key as the word name
Its value is the highest occurring matching POS in the training data for that word.
'''
def buildBaseLine(fileContent):

    for line in fileContent:
            column = line.split()
            if column:
                sl = column[0]
                word = column[1]
                pos = column[2]
                if word in word_pos_tags:
                    if pos in word_pos_tags[word]:
                        (word_pos_tags[word])[pos] +=  1
                    else:
                        (word_pos_tags[word])[pos] = 1
                else:
                    posCounts = dict()
                    posCounts[pos] = 1
                    word_pos_tags[word] = posCounts

                #extract total occurences of a word in the given data
                global word_counts
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

    #assign words with the highest occurring POS
    for key in word_pos_tags:
        most_frequent_tags[key] = max(word_pos_tags[key], key=word_pos_tags[key].get)
        word_counts_sorted = sorted(word_counts.items(), key=operator.itemgetter(1))


def splitFiles(trainingInputContentToSplit):
    if not (os.path.isfile(testFile) and os.path.isfile(testExpectedFile) and os.path.isfile(trainingFile)):
        train, test = train_test_split(trainingInputContentToSplit, test_size=0.2)
        trainingfileObj = open(trainingFile, 'w')
        testExpectedFileObj = open(testExpectedFile,'w')
        testfileObj = open(testFile, 'w')

        for line in test:
            sentences = line.strip().split(',')
            if line.strip():
                sentences = line.strip().split(',')
                for each in sentences:
                    testExpectedFileObj.write(each.strip() + '\n')
                testExpectedFileObj.write('\n')

        for line in train:
            sentences = line.strip().split(',')
            if line.strip():
                sentences = line.strip().split(',')
                for each in sentences:
                    trainingfileObj.write(each.strip() + '\n')
                trainingfileObj.write('\n')

        for line in test:
            sentences = line.strip().split(',')
            if line.strip():
                sentences = line.strip().split(',')
                for each in sentences:
                    column = each.split('\t')
                    if (len(column) == 3):
                        testfileObj.write(column[0] + "\t" + column[1] + '\n')
                testfileObj.write('\n')


if __name__ == "__main__":
    trainingInputContent = open(InputFileName, 'r').readlines()

    # Each sentence is put into one single line as we will split data randomly
    sentenceArray = arrangeSentencesInEachLine(trainingInputContent)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Split files into training and test
    splitFiles(sentenceArray)
	#buildBaseLine(trainingInputContent)
