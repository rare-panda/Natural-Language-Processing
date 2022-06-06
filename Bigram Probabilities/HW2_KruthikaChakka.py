
import nltk as nltk
import sys




# Press the green button in the gutter to run the script.
def readTokens(file):
    tokens = {};
    for line in file:
        line = line.lower()
        words = line.split(" ")
        for word in words:
            token = word.split("_", 1)[0]
            if token in tokens:
                tokens[token] += 1;
            else:
                tokens[token] = 1;
    return tokens


def createBigram(file):
    unigrams = []
    bigrams = []
    unigramsCount = {}
    bigramsCount = {}
    biNcountList = {}
    uniNcountList = {}
    for line in file:
        line = line.lower()
        words = line.split(" ")
        #Bigrams per each line
        for i in range(len(words)):
            if i < len(words)-1:
               prev_word = words[i].split("_")[0];
               curr_word = words[i+1].split("_")[0];
               unigrams.append(prev_word)
               bigrams.append((prev_word,curr_word))
            unigrams.append(words[len(words)-1])
    #Unigrams count over all lines
    for unigram in unigrams:
        if unigram in unigramsCount:
            unigramsCount[unigram] += 1;
        else:
            unigramsCount[unigram] = 1;
    #Unigram N count list
    for x in unigramsCount.values():
        if x in uniNcountList:
            uniNcountList[x] += 1;
        else:
            uniNcountList[x] = 1;
    #Bigrams count over all lines
    for bigram in bigrams:
        if bigram in bigramsCount:
                bigramsCount[bigram] += 1;
        else:
                bigramsCount[bigram] = 1;
    #Bigram N count list
    for x in bigramsCount.values():
        if x in biNcountList:
            biNcountList[x] += 1;
        else:
            biNcountList[x] = 1;
    biNcountTotal = len(bigramsCount)
    uniNcountTotal = len(unigramsCount)
    return unigrams, bigrams, unigramsCount, bigramsCount, uniNcountTotal, uniNcountList, biNcountTotal, biNcountList


def calcBigramProb(bigrams, bigramsCount, unigramsCount):
    bigramsProb = {}
    for bigram in bigrams:
        if bigram not in bigramsProb:
            prev_word = bigram[0]
            bigramsProb[bigram] = bigramsCount[bigram]/unigramsCount[prev_word]
    file = open('bigramProb.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')
    for bigram in bigramsCount:
        file.write(str(bigram) + '  :  ' + str(bigramsCount[bigram])
                   + '  :  ' + str(bigramsProb[bigram]) + '\n')
    return bigramsProb


def calAddOneProb(bigrams, bigramsCount, unigramsCount, uniNcountTotal):
    bigramsAddOneProb = {}
    for bigram in bigrams:
        if bigram not in bigramsAddOneProb:
            prev_word = bigram[0]
            bigramsAddOneProb[bigram] = (bigramsCount[bigram]+1)/(unigramsCount[prev_word]+uniNcountTotal)
    file = open('addOneProb.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'Probability' + '\n')
    for bigram in bigramsCount:
        file.write(str(bigram) + '  : ' + str(bigramsAddOneProb[bigram]) + '\n')
    return bigramsAddOneProb


def calGTProb(bigrams, bigramsCount, unigrams, unigramsCount, uniNcountList, uniNcountTotal, biNcountList, biNcountTotal):
    c_star = {}
    goodTuringProb = {}
    for bigram in bigrams:
        if bigram not in goodTuringProb:
            c = bigramsCount[bigram]
            if c == 0:
               # n1/N_bi
                goodTuringProb[bigram] = biNcountList[1]/biNcountTotal
            else:
                if c+1 not in biNcountList:
                    c_star[bigram] = 0
                    # n1/N_bi
                    goodTuringProb[bigram] = biNcountList[1]/biNcountTotal
                else:
                    # (c+1)(Nc+1)/Nc
                    c_star[bigram] = (c + 1)*biNcountList[c+1]/biNcountList[c]
                    # c_*/N_bi
                    goodTuringProb[bigram] = c_star[bigram]/biNcountTotal
    file = open('GoodTuring.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'C_star' + '\t' + 'Probability' + '\n')
    for bigram in bigramsCount:
        file.write(str(bigram) + '  :  ' + str(c_star[bigram]) + '  :  ' + str(goodTuringProb[bigram]) + '\n')
    return c_star, goodTuringProb


def testNoSmoothing(input_line, unigrams, unigramsCount, bigramsCount):
    prob = 1
    words = input_line.split(" ")
    if words[0] not in unigramsCount:
        prob *= 0;
    else:
        prob *= unigramsCount[words[0]]/len(unigrams)
    for i in range(len(words)):
        if i < len(words) - 1:
            new_bigram = (words[i], words[i+1])
            if new_bigram not in bigramsCount:
                return 0;
            else:
                prob *= bigramsCount[new_bigram]/unigramsCount[words[i]]
    return prob


def testAddOne(input_line, unigramsCount, bigramsCount, uniNcountTotal):
    prob = 1
    words = input_line.split(" ")

    #if len(words) > 0:
       # prob *= unigramsCount[words[0]]/len(unigrams)

    for i in range(len(words)):
        if i < len(words) - 1:
            new_bigram = (words[i], words[i + 1])
            if new_bigram not in bigramsCount:
                    prob *= (1) / (unigramsCount[words[i]] + uniNcountTotal);
            else:
                prob *= (bigramsCount[new_bigram] + 1) / (unigramsCount[words[i]] + uniNcountTotal)
    return prob


def testGT(input_line, unigramsCount, bigramsCount, uniNcountList, uniNcountTotal, biNcountList, biNcountTotal):
    prob = 1
    words = input_line.split(" ")
   
    if len(words) > 0:
        prob *= uniNcountList[1] / len(unigrams);


    for i in range(len(words)):
        if i < len(words) - 1:
            new_bigram = (words[i], words[i + 1])
            if new_bigram not in bigramsCount:
                prob *= biNcountList[1]/biNcountTotal
            else:
                c = bigramsCount[new_bigram];
                if c+1 not in biNcountList:
                    prob *= biNcountList[1] /biNcountTotal
                else:
                    c_star_value = (c + 1) * biNcountList[c + 1] / uniNcountList[c]
                    prob *= c_star_value/biNcountTotal
    return prob


if __name__ == '__main__':
    input_training_file_path = input("Enter training data file path : ")
    file = open(input_training_file_path,"r")
    unigrams, bigrams, unigramsCount, bigramsCount, uniNcountTotal, uniNcountList, biNcountTotal, biNcountList = createBigram(file)
    prob = calcBigramProb(bigrams,bigramsCount, unigramsCount)
    addOneProb = calAddOneProb(bigrams, bigramsCount, unigramsCount, uniNcountTotal)
    c_star, goodTuringProb = calGTProb(bigrams, bigramsCount, unigrams, unigramsCount, uniNcountList, uniNcountTotal, biNcountList, biNcountTotal)


    input_line = input("Enter the input line to test : ") 
    smoothing_technique = input("Enter Smoothing Technique serial Number: 1. No Smoothing, 2. Add one smoothing, 3. Good Turing Smoothing :")
    if len(input_line) < 1:
        print("Please run program again and enter a input sentence to test!!!")
        exit()
    else:
        if smoothing_technique == "1":  # 0
            test_prob = testNoSmoothing(input_line, unigrams, unigramsCount, bigramsCount)
        elif smoothing_technique == "2":  # 0.00013140604467805518    #6.584694494726948e-09
            test_prob = testAddOne(input_line, unigramsCount, bigramsCount, uniNcountTotal)
        elif smoothing_technique == "3":  # 0.5843030453082446    #0.013121241092186946
            test_prob = testGT(input_line, unigramsCount, bigramsCount, uniNcountList, uniNcountTotal, biNcountList, biNcountTotal)
        else:
            print("Please run program again and enter a  valid smoothing technique index.")
            exit()
        print(test_prob)
