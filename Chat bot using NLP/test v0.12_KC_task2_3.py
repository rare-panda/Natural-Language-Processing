# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import nltk
import os # To read all txt files
from nltk.corpus import wordnet as wn #Wordnet inteface
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy as np
from nltk.parse.stanford import StanfordDependencyParser
from itertools import chain
import spacy 
import en_core_web_sm
nlp = spacy.load("en_core_web_sm")

def read_txt_file(file_path):
    with open(file_path,'r',encoding="utf8", errors='ignore') as f:
        return(f.read().strip())

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    if word.startswith('J'):
        return wn.ADJ
    elif word.startswith('V'):
        return wn.VERB
    elif word.startswith('N'):
        return wn.NOUN
    elif word.startswith('R'):
        return wn.ADV
    else:
        return ''

#-----------Generate multiple quetions from a question----------------
def pre_process_question(ques):
    versions = []
    words = word_tokenize(ques)
    tagged = nltk.pos_tag(words)
    
    for word in tagged:
        pos = get_wordnet_pos(word[1])
        synonyms = []
        hypernyms = []
        hyponyms = []
        antonyms = []
        
        if pos == "v" or pos == "n":
            for i,j in enumerate(wn.synsets(word[0])):
                for synin in wn.synsets("good"):    
                    synonyms.append([str(l.name()) for l in j.lemmas()])
                # antonyms.append([str(l.name()) for l in j.lemmas()])
                # hypernyms.extend(list(chain(*[l.lemma_names() for l in j.hypernyms()])))
                # hyponyms.extend(list(chain(*[l.lemma_names() for l in j.hyponyms()])))


            for m in range(len(synonyms)):
                for syn in synonyms[m]:
                    new_ver = ques.replace(word[0],syn)
                    if new_ver not in versions: versions.append(new_ver)
            # for hyn in hypernyms:
            #     versions.append(ques.replace(word[0],hyn))
            # for hyp in hyponyms:
            #     versions.append(ques.replace(word[0],hyp))
            # for tp in toponyms:
            #     versions.append(ques.replace(word[0],tp))
    versions.append(ques)
    return(versions)


def cosine_cal(qu, sent):
    q = set(qu.split(' '))
    s = set(sent.split(' '))
    l1 =[]
    l2 =[]
    rvector = q.union(s) 
    #creating vector
    for w in rvector:
        if w in qu: 
            l1.append(1) # create a vector
        else: 
            l1.append(0)
        if w in sent: 
            l2.append(1)
        else: l2.append(0)
    c = 0

    # cosine formula 
    for i in range(len(rvector)):
        cosine = 0
        c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine


# ---------------------------Main function--------------------------------------------------------
if __name__ == '__main__':
    questions = nltk.tokenize.sent_tokenize(read_txt_file(os.getcwd()+ "\\questions.txt"))
    #task1(os.getcwd() + "/Task1_file.txt")
    
    #--------------Variables---------------------------
    dataset=[]
    # df={}
    # tf_idf={}
    doc_info = []#list of lists: doc index, doc title, doc content, sentences, words in doc, preprocessed words in the doc
    for i in range(5):
        doc_info.append([])
    docs = []
    N=len(os.listdir())
    stop_words=stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    
    #--------------folder path-----------------------
    folderpath = os.getcwd() + "\\articles"
    #---------------change directoty-----------------
    os.chdir(folderpath)    
    #----------iterate through each file-------------
    
    for file in os.listdir():
        lemmas = []
        
        sentences = []
        tagged_sentences = []
        doc_info[0].append(str(file))  #**first list in doc_info is the file name of the docs**
        dataset.append(str(file))
        
        text = read_txt_file(file) #**second list in doc_info is the file content of the docs**
        doc_info[1].append(text)
        
        sentences = nltk.tokenize.sent_tokenize(text)
        doc_info[2].append(sentences)   #**third list in doc_info is the sentences in doc**
        
        words=word_tokenize(text)
        doc_info[3].append(words) #**fourth list in doc_info is the words in doc**
        
        new_text = ""
        
        for word in words:
            if word not in stop_words:
                new_text = new_text + " " + word
        lemmatized_output = [lemmatizer.lemmatize(w) for w in word_tokenize(new_text)]              
        doc_info[4].append(lemmatized_output) #fifth list in doc_info is the preprocessed text in doc
                                    #Stop words and symbols removed
    
    answers = []
    cosine = 0
    doc_ids = []
    sentence = ''
    sentence_list=[]
    for query in questions:
        # query='Who mediated the truce with Khomeini?'
        max_cosine=-10000
        symbols = "!\"#$%&()*+./:;<=>?@[\]^`{|}~\n"
        for i in symbols:
            query = query.replace(i, '')
        lemmatized_sentence = []
        lemmatized_sentence = [lemmatizer.lemmatize(w) for w in word_tokenize(query)] 
        print('Lemmatized Sentence: \n', lemmatized_sentence) 

        antonyms= []  
        synonyms= []
        new_query=""
        query_token=word_tokenize(query)
        for word in query_token:
            if word not in stop_words:
                new_query=new_query+" "+word
        print('Lemmatized Sentence: \n', new_query) 
        doc = nlp(new_query)
        # Token and Tag
        proper_nouns = []
        common_nouns = []
        verbs=[]
        for token in doc:
            if token.pos_ == 'PROPN':
                proper_nouns.append(str(token))
            elif token.pos_ == 'NOUN':
                common_nouns.append(str(token))
            elif token.pos_=='VERB':
                verbs.append(str(token))
                for syn in wn.synsets(str(token)):
                    for l in syn.lemmas():
                        synonyms.append(l.name())
                    if l.antonyms():
                        antonyms.append(l.antonyms()[0].name())
        
        print('Proper Noun: ', proper_nouns)
        print('Common Noun: ', common_nouns)
        print('Verbs: ', verbs)
        print('Synonyms: ', synonyms)
        print('Antonyms: ', antonyms)
        # query = ""
        # for word in lemmatized_sentence:
        #         if word.lower() not in stop_words:
        #             query = query + " " + word
        flag_common_count = 0
        flag_cosine_proper = 0
        versions = pre_process_question(query)
        
        for doc in range(len(doc_info[2])):    
            for sent in doc_info[2][doc]:
                for qu in versions:
                    flag_proper = 0  
                    
                    similar_nouns = 0
                    sente=sent #sente -->sentence before we remove stopwords and symbols
#                     sent = sent.lower()
                    #removing symbols from sentence
                    symbols = "!\"#$%&()*+./:;<=>?@[\]^`{|}~\n"
                    for i in symbols:
                        sent = sent.replace(i, '')
                        qu = qu.replace(i, '')
                        
                    #lemmatizing sentences in document
                    lemmatized_sent = [lemmatizer.lemmatize(w) for w in word_tokenize(sent)]
                    
                    
                    #converting strings to set of words so union can be performed
                    counter_proper_nouns = 0
                    counter_common_nouns = 0
                    if len(proper_nouns) > 0: 
                        flag_proper = 1
                    for i in proper_nouns:
                        if i in lemmatized_sent:
                            counter_proper_nouns += 1
                    
                
                    for i in common_nouns:
                        if i in lemmatized_sent:
                            counter_common_nouns += 1
                    
                    
                    if len(proper_nouns) > 0:
                        if counter_proper_nouns == len(proper_nouns):                 
                            cosine = cosine_cal(qu, sent)
                            if flag_cosine_proper < cosine:
                                sentence = sente
                                sentence_list.append(sentence)
                                doc_id = doc_info[0][doc]
                                flag_cosine_proper = cosine
                        
                        elif counter_common_nouns > 1:
                            cosine = cosine_cal(qu, sent)
                            if flag_cosine_proper < cosine:
                                sentence = sente
                                sentence_list.append(sentence)
                                doc_id = doc_info[0][doc]
                                flag_cosine_proper = cosine
                        
                    elif counter_common_nouns > 0 and flag_proper != 1:
                        if counter_common_nouns > flag_common_count: 
                            flag_common_count = counter_common_nouns
                            cosine = cosine_cal(qu, sent)
                            sentence = sente
                            sentence_list.append(sentence)
                            doc_id = doc_info[0][doc]

        answers.append(sentence)
        doc_ids.append(doc_id)
        
    #----------------Write answers into CSV file----
    df = pd.DataFrame(list(zip(*[questions, answers, doc_ids])))
    df.to_csv('answers.csv', index=False)
    print(df)

