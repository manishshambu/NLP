import re
import operator
import os.path
from sklearn.model_selection import train_test_split

most_frequent_tags = dict()
word_pos_tags = dict()
word_counts = dict()
pos_counts = dict()
InputFileName = "berp-POS-training-small.txt"
testFileName = "berp-POS-test.txt"
testFileName = "berp-POS-test.txt"
dir_path = ""
trainingFile = "training.txt"
testExpectedFile = "test_expected.txt"
testFile = "test.txt"
prefix_pattern = "(^[0-9])"
observationSpace = set()
wordOrderList = list()
posOrderList = list()
transitional_p = dict()
emmision_p = dict()
stateBigramTransitionCounts = dict()
start_p = dict()

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
    global stateSpace
    global observationSpace
    global word_counts
    global pos_counts

    wordOrderList.append('.')
    posOrderList.append('.')

    for line in fileContent:
            column = line.split()
            if column:
                sl = column[0]
                word = column[1]
                pos = column[2]
                wordOrderList.append(word)
                posOrderList.append(pos)
                if word in word_pos_tags:
                    if pos in word_pos_tags[word]:
                        (word_pos_tags[word])[pos] +=  1
                    else:
                        (word_pos_tags[word])[pos] = 1
                else:
                    posCounts = dict()
                    posCounts[pos] = 1
                    word_pos_tags[word] = posCounts

                #extract total occurences of a words and POS in the given data
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
                if pos in pos_counts:
                    pos_counts[pos] += 1
                else:
                    pos_counts[pos] = 1

    #assign words with the highest occurring POS
    for key in word_pos_tags:
        most_frequent_tags[key] = max(word_pos_tags[key], key=word_pos_tags[key].get)

    observationSpace = set(word_pos_tags.keys())
    stateSpace = set(pos_counts.keys())


def splitFiles(trainingInputContentToSplit):
    if not (os.path.isfile(testFile) and os.path.isfile(testExpectedFile) and os.path.isfile(trainingFile)):
        train, test = train_test_split(trainingInputContentToSplit, test_size=0.1)
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

def buildBigrams(input_list):
    return zip(input_list, input_list[1:])

def generateBigramTransitionCounts(bigramsTuple, space):
    global stateBigramTransitionCounts
    for i in space:
        stateBigramTransitionCounts[i] = dict()
        for j in space:
            (stateBigramTransitionCounts[i])[j] = 0

    for each in bigramsTuple:
         if each[0] in stateBigramTransitionCounts:
             if each[1] in  stateBigramTransitionCounts[each[0]]:
                 (stateBigramTransitionCounts[each[0]])[each[1]] += 1
             else:
                 (stateBigramTransitionCounts[each[0]])[each[1]] = 1
         else:
             (stateBigramTransitionCounts[each[0]])[each[1]] = 1
    print(stateBigramTransitionCounts)

def generateTransitionProbablilities(transitionCounts, space):
    global transitional_p
    for i in space:
        transitional_p[i] = dict()
        for j in space:
            (transitional_p[i])[j] = 0

    for state in transitionCounts:
        #print(state)
        totalTransitions = 0
        for transitions in transitionCounts[state]:
            totalTransitions += transitionCounts[state][transitions]

        for transitions in transitionCounts[state]:
            (transitional_p[state])[transitions] = (transitionCounts[state][transitions])/totalTransitions
    #print(transitional_p)

def checkProbabilities(transitional_p):
    flag = 1
    for each in transitional_p:
        if sum(transitional_p[each].values()) < 0.999 and sum(transitional_p[each].values()) > 1.001:
            return 0
    return flag

def generateEmmisionCounts(observationSpace, stateSpace):
    emmisionBigramTransitionCounts = dict()
    for i in stateSpace:
        emmisionBigramTransitionCounts[i] = dict()
        for j in observationSpace:
            (emmisionBigramTransitionCounts[i])[j] = 0

    emmisionList = zip(posOrderList, wordOrderList)

    for each in emmisionList:
        if each[0] in emmisionBigramTransitionCounts:
            if each[1] in emmisionBigramTransitionCounts[each[0]]:
                (emmisionBigramTransitionCounts[each[0]])[each[1]] += 1
            else:
                (emmisionBigramTransitionCounts[each[0]])[each[1]] = 1
        else:
            (emmisionBigramTransitionCounts[each[0]])[each[1]] = 1
    return emmisionBigramTransitionCounts

def generateEmmisionProbablilities(emmissionCounts, observationSpace, stateSpace):
    global emmision_p

    for i in stateSpace:
        emmision_p[i] = dict()
        for j in observationSpace:
            (emmision_p[i])[j] = 0

    for state in emmissionCounts:
        for word in emmissionCounts[state]:
            (emmision_p[state])[word] = (emmissionCounts[state][word]) / word_counts[word]

def generateStartProbabilities():
    bigramtuples = zip(wordOrderList, posOrderList[1:])
    start_count = dict()
    for i in stateSpace:
        start_count[i] = 0

    for i in bigramtuples:
        if i[0] == '.':
            start_count[i[1]] += 1

    totalStarts = sum(start_count.values())

    for pos in start_count:
        prob = start_count[pos]/totalStarts
        start_p[pos] = prob

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t - 1][prev_st]["prob"] * trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t - 1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    for line in dptable(V):
        pass
        #print(line)
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    return opt
    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)

def buildTestObservationInOrder(content):
    testObservation = list()
    for line in content:
        column = line.split()
        if column:
            testObservation.append(column[1])
    return testObservation

def writeOutputFile(testFile, outputFile, opt):
    testFileObj = open(testFile, 'r')
    outputFileObj  = open(outputFile, 'w')
    for line in testFileObj.readlines():
        column = line.split()
        if column:
            sl = column[0]
            word = column[1]
            pos = opt.pop(0)
            writeline = sl+'\t'+word+'\t'+pos+'\n'
            outputFileObj.write(writeline)
        else:
            outputFileObj.write('\n')
    outputFileObj.close()

def addKSmoothing(discount):
    for state1 in stateBigramTransitionCounts:
        for state2 in stateBigramTransitionCounts[state1]:
            stateBigramTransitionCounts[state1][state2] += discount
    #print(stateBigramTransitionCounts)

def handleUnknowns(trainingContent, testContent):
    for column in testFile:
        pass



if __name__ == "__main__":
    trainingInputContent = open(InputFileName, 'r').readlines()

    # Each sentence is put into one single line as we will split data randomly
    sentenceArray = arrangeSentencesInEachLine(trainingInputContent)

    # Split files into training and test
    #splitFiles(sentenceArray)
    trainingContent = open(trainingFile, 'r').readlines()
    testContent = open(testFile, 'r').readlines()

    buildBaseLine(trainingContent)

    handleUnknowns(testContent, trainingContent)

    stateBigrams = buildBigrams(posOrderList)
    generateBigramTransitionCounts(stateBigrams,stateSpace)

    discount = 0.75
    addKSmoothing(discount)

    generateTransitionProbablilities(stateBigramTransitionCounts, stateSpace)
    correct = checkProbabilities(transitional_p)

    emmisionBigramTransitionCounts = generateEmmisionCounts(observationSpace, stateSpace)
    generateEmmisionProbablilities(emmisionBigramTransitionCounts, observationSpace, stateSpace)
    correct = checkProbabilities(emmision_p)

    generateStartProbabilities()

    testObservationInOrder = buildTestObservationInOrder(testContent)

    opt = viterbi(testObservationInOrder, list(stateSpace), start_p, transitional_p, emmision_p)

    outputFileName = 'shambumuralidhar-manish-assgn2-test-output.txt'
    writeOutputFile(testFile, outputFileName, opt)






