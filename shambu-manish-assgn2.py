import re
import operator




most_frequent_tags = dict()
word_pos_tags = dict()
word_counts = dict()
word_counts_sorted = dict()

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
def buildBaseLine(filename):
    s = open(filename, 'r')

    for line in s.readlines():
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




if __name__ == "__main__":
	posFileName = "berp-POS-training.txt"
	buildBaseLine(posFileName)
