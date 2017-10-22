from sklearn.model_selection import train_test_split
import math
from random import shuffle
import operator

prefix_pattern = "(^[0-9])"
posInputFileName = "hotelPosT-train.txt"
negInputFileName = "hotelNegT-train.txt"

classLabels = ['POS', 'NEG']

# Splits the training data into test and development data
def splitFiles(trainingData):
    return train_test_split(list(trainingData), test_size = 0.1)

def getVocabulary(content):
    wordCountDict = dict()

    for each in content:
        ID = each.split()[0]
        words = each.split()[1:]

        for word in words:
            if word in wordCountDict:
                wordCountDict[word] += 1
            else:
                wordCountDict[word] = 1

    return wordCountDict

def trainNaiveBayes(class1docs, class2docs):
    logprior = dict()
    loglikelihood = {'POS': {}, 'NEG': {}}
    N = dict()
    N[classLabels[0]] = class1docs.__len__()
    N[classLabels[1]] = class2docs.__len__()

    totaldocs = N[classLabels[0]] + N[classLabels[1]]
    logprior[classLabels[0]] = math.log(N[classLabels[0]]/totaldocs)
    logprior[classLabels[1]] = math.log(N[classLabels[1]]/totaldocs)

    vocabulary = getVocabulary(class1docs + class2docs)

    vocabularyPos = getVocabulary(class1docs)
    vocabularyNeg = getVocabulary(class2docs)

    count = {}
    count[classLabels[0]] = {}
    count[classLabels[1]] = {}

    for eachWord in vocabulary.keys():
        if eachWord not in vocabularyPos:
            count['POS'][eachWord] = 0
        else:
            count['POS'][eachWord] = vocabularyPos[eachWord]
        if eachWord not in vocabularyNeg:
            count['NEG'][eachWord] = 0
        else:
            count['NEG'][eachWord] = vocabularyNeg[eachWord]

        loglikelihood['POS'][eachWord] = math.log((count['POS'][eachWord] + 1) / ( sum(vocabularyPos.values()) + len(vocabulary)) )
        loglikelihood['NEG'][eachWord] = math.log((count['NEG'][eachWord] + 1) / ( sum(vocabularyNeg.values()) + len(vocabulary)) )

    return logprior, loglikelihood, vocabulary


def classifyTestSentiment(testContent, loglikelihood, logprior, vocabulary):
    outputList = []
    for eachLine in testContent:
        bestClass = testNaiveBayes(eachLine.split()[1:], loglikelihood, logprior, vocabulary)
        outputList.append(eachLine.split()[0] +"\t"+ bestClass)
    writeFile(outputList, "output.txt", '\n')


def testNaiveBayes(testSentence, loglikelihood, logprior, vocabulary):
    totalSum = {}
    for eachClass in classLabels:
        totalSum[eachClass] = logprior[eachClass]

        for word in testSentence:
            if word in vocabulary:
                totalSum[eachClass] = totalSum[eachClass] + loglikelihood[eachClass][word]

    return max(totalSum.__iter__(), key=lambda k: totalSum[k] )

def writeFile(content, fileName, separator):
    fObj = open(fileName, 'w')
    fObj.write(separator.join(content))


if __name__ == "__main__":
    trainingInputContentPositive = open(posInputFileName, 'r').readlines()
    trainingInputContentNegative = open(negInputFileName, 'r').readlines()

    sentenceArrayPositiveDev, sentenceArrayPositiveTest = splitFiles(trainingInputContentPositive)
    sentenceArrayNegativeDev, sentenceArrayNegativeTest = splitFiles(trainingInputContentNegative)

    testSentences = sentenceArrayPositiveTest + sentenceArrayNegativeTest
    shuffle(testSentences)

    writeFile(sentenceArrayPositiveDev, "PosDevData.txt", "")
    writeFile(sentenceArrayNegativeDev, "NegDevData.txt", "")
    writeFile(testSentences, "TestData.txt", "")

    logprior, loglikelihood, vocabulary = trainNaiveBayes(sentenceArrayPositiveDev, sentenceArrayNegativeDev)
    classifyTestSentiment(testSentences, loglikelihood, logprior,vocabulary)







