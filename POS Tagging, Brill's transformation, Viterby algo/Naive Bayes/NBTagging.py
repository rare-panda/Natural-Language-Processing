
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


def createBigramWithPOS(file):
    wordCount = {}
    tagCount = {}
    wordTagCount = {}
    prevCurrTagCount = {}
    wordTagProb = {}
    prevCurrTagCountProb = {}
    prev_tag = None
    for line in file:
        wordTags = line.split(" ")

        for wordTag in wordTags:
            wordArr = wordTag.split("_")
            word = wordArr[0]
            if len(wordArr) > 1:
                tag = wordArr[1]
            if word in wordCount:
                wordCount[word] = wordCount.get(word, 0) + 1
            else:
                wordCount[word] = 1
            if tag in tagCount:
                tagCount[tag] = tagCount.get(tag) + 1
            else:
                tagCount[tag] = 1
            if word in wordTagCount:
                if tag in wordTagCount[word].keys():
                    wordTagCount[word][tag] = wordTagCount[word].get(tag) + 1
                else:
                    wordTagCount[word][tag] = 1;
            else:
                wordTagCount[word] = {}
                wordTagCount[word][tag] = 1
            if prev_tag != None:
                prevCurrTagCount[(prev_tag, tag)] = prevCurrTagCount.get((prev_tag, tag), 0) + 1
            prev_tag = tag
        prev_tag = None
    for word in wordTagCount:
        for tag in wordTagCount[word].keys():

            wordTagProb[(word, tag)] = (wordTagCount[word][tag])/(tagCount[tag])
    for prevCurr in prevCurrTagCount:
        prevCurrTagCountProb[prevCurr] = prevCurrTagCount[prevCurr]/tagCount[prevCurr[0]]



    return wordCount, tagCount, wordTagCount, prevCurrTagCount, wordTagProb, prevCurrTagCountProb


def calBigramProbPOS(wordCount, tagCount, wordTagCount, prevCurrTagCount, wordTagProb, prevCurrTagCountProb,
                     input_line):
    NB_Sentence_WT = []
    NB_SentenceT = []
    sentWords = input_line.split()
    sentenceWords = input_line.split()
    for word_tag in sentWords:
        word = word_tag.split('_')[0]
        if word in wordTagCount:
            NB_SentenceT.append(list(wordTagCount[word].keys()))
        else:
            NB_SentenceT.append(list('NN'))
        NB_Sentence_WT.append([word, None])
    
    combinations = [[]]

    for x in NB_SentenceT:
        combinations = [i + [y] for y in x for i in combinations]
        


    comb_prob = []
    for i, j in enumerate(combinations):
        num = wordTagCount.get(sentenceWords[0].split('_')[0], 0).get(j[0], 0)
        den = tagCount.get(j[0], 0)
        if num == 0 or den == 0:
            comb_prob.append(0)
        else:
            comb_prob.append(float(num) / float(den))
    

    comb_prob = []
    for i, j in enumerate(combinations):
        num = wordTagCount.get(sentenceWords[0].split('_')[0], 0).get(j[0], 0)
        den = tagCount.get(j[0], 0)
        if num == 0 or den == 0:
            comb_prob.append(0)
        else:
            comb_prob.append(float(num) / float(den))

    for i, j in enumerate(combinations):
        totalprob = 1
        t = 1
        while (t < len(j) - 1):
            num1 = wordTagCount.get(sentenceWords[t].split('_')[0], 0).get(j[t], 0)
            den1 = tagCount.get(j[t], 0)
            num2 = prevCurrTagCount.get((j[t - 1], j[t]), 0)
            den2 = tagCount.get(j[t], 0)

            if num1 == 0 or num2 == 0 or den1 == 0 or den2 == 0:
                totalprob = 0
                break
            else:
                totalprob = totalprob * (float(num1) / float(den1)) * (float(num2) / float(den2))
            t += 1
        comb_prob[i] = comb_prob[i] * totalprob

    m = 0
    max_index = 0
    i = 0
    while (i < len(combinations) - 1):
        if comb_prob[i] > m:
            m = comb_prob[i]
            max_index = i
        i += 1

    for i, j in enumerate(combinations[max_index]):
        NB_Sentence_WT[i][1] = j

    print("\n Naive Bayes POS Tagged Sentence \n")
    for i in NB_Sentence_WT:
        print(i[0] + "_" + i[1], end=" ")
    print(end="\n")
    return NB_SentenceT


if __name__ == '__main__':
    input_training_file_path = input("Enter training data file path : ")

    file = open(input_training_file_path,"r")
    wordCount, tagCount, wordTagCount, prevCurrTagCount, wordTagProb, prevCurrTagCountProb = createBigramWithPOS(file)

    input_line = input("Enter the input line to test : ")
    taqSeq = calBigramProbPOS(wordCount, tagCount, wordTagCount, prevCurrTagCount, wordTagProb, prevCurrTagCountProb,input_line)




