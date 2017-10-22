def evaluateOutput(outputContent, negData, posData):
    posIds = []
    negIds = []
    correct = 0
    total = 0
    for line in posDevData:
        posIds.append(line.split()[0])

    for line in negDevData:
        negIds.append(line.split()[0])

    #print(posIds)
    #print(negIds)

    for line in outputContent:
        total = total + 1
        id, bestClass = line.split()
        #print(id)
        #print(bestClass)
        if bestClass == 'POS' and id in posIds:
            correct = correct + 1

        if bestClass == 'NEG' and id in negIds:
            correct = correct + 1

    print(correct/total)




if __name__ == "__main__":
    outputfile = open("output.txt", 'r').readlines()
    negDevData = open("hotelNegT-train.txt", 'r').readlines()
    posDevData = open("hotelPosT-train.txt", 'r').readlines()
    evaluateOutput(outputfile, negDevData, posDevData)