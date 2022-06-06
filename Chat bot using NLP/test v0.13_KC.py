
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


# import urllib.request
# import zipfile
# urllib.request.urlretrieve(r'http://nlp.stanford.edu/software/stanford-postagger-full-2015-04-20.zip', r'C:/Users/srini/Downloads/stanford-postagger-full-2015-04-20.zip')
# zfile = zipfile.ZipFile(r'C:/Users/srini/Downloads/stanford-postagger-full-2015-04-20.zip')
# zfile.extractall(r'C:/Users/srini/Downloads/')

# set STANFORDTOOLSDIR=$HOME
# set CLASSPATH=$STANFORDTOOLSDIR/stanford-postagger-full-2015-04-20/stanford-postagger.jar
# set export STANFORD_MODELS=$STANFORDTOOLSDIR/stanford-postagger-full-2015-04-20/models

# java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
# os.environ['JAVAHOME'] = java_path

# path_to_jar = os.getcwd() + '/stanford-parser-4.2.0/stanford-parser-full-2020-11-17/stanford-parser.jar'
# path_to_models_jar = os.getcwd() + '/stanford-parser-4.2.0/stanford-parser-full-2020-11-17/stanford-parser-4.2.0-models.jar'
# dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)


#------------Read a text file and return the text of file----------
def read_txt_file(file_path):
    with open(file_path,'r',encoding="utf8", errors='ignore') as f:
        return(f.read().strip())

#------------Read a text file and return the text of file----------
def task1(file_path):
    lemmatizer = WordNetLemmatizer()
    synonyms = []
    lemmas = []
    hyponyms = []
    hypernyms = []
    holonyms = []
    meronyms = []
    file1 = open(r"lemmas.txt","w")
    
   
    with open(file_path,'r',encoding="utf8", errors='ignore') as f:
        text=f.read()
        sentence_text = nltk.tokenize.sent_tokenize(text)
        word_token = nltk.word_tokenize(text)  #Tokenize the file 
        tagged = nltk.pos_tag(word_token)
       
        file1.write("".join('Tokenized Sentences are:\n'))
        file1.write("\n".join(str(item) for item in sentence_text))
        file1.write("".join('\n\n'))
        file1.write("".join('Tokenized Words are:\n'))
        file1.write("\n".join(str(item) for item in word_token))
        file1.write("".join('\n\n'))
        file1.write("".join('POS Tagged words are:\n'))
        file1.write("\n".join(str(item) for item in tagged))
        file1.write("".join('\n\n'))
        file1.write("".join('Dependency parsed sentences are:\n'))
        
        # for sentence in sentence_text:
        #     result = dependency_parser.raw_parse('I shot an elephant in my sleep')
        #     dep = result.next()
        #     # file1.write("\n".join(list(dep.triples())))
        #     print(result)
        
        
        for word in word_token:
            lemmas.append(lemmatizer.lemmatize(word))
            for i,j in enumerate(wn.synsets(word)):
                # synonymns_list.extend(wn.synset(j.name()).lemma_names())
                synonyms.append([str(l.name()) for l in j.lemmas()])
                hypernyms.extend(list(chain(*[l.lemma_names() for l in j.hypernyms()])))
                hyponyms.extend(list(chain(*[l.lemma_names() for l in j.hyponyms()])))
                meronyms.extend(list(chain(*[l.lemma_names() for l in j.part_meronyms()])))
                holonyms.extend(list(chain(*[l.lemma_names() for l in j.part_holonyms()])))
        
       
    file1.write("".join('Lemmas are:\n'))
    file1.write("\n".join(str(item) for item in lemmas))
    file1.write("".join('\n\n'))
    file1.write("".join('Synonyms are:\n'))
    file1.write("\n".join(str(item) for item in synonyms))
    file1.write("".join('\n\n'))
    file1.write("".join('hyponyms are:'))
    file1.write("\n".join(str(item) for item in hyponyms))
    file1.write("".join('\n\n'))
    file1.write("".join('hypernyms are:\n'))
    file1.write("\n".join(str(item) for item in hypernyms))
    file1.write("".join('\n\n'))
    file1.write("".join('holonyms are:\n'))
    file1.write("\n".join(str(item) for item in holonyms))
    file1.write("".join('\n\n'))
    file1.write("".join('meronyms are:\n'))
    file1.write("\n".join(str(item) for item in meronyms))
    file1.write("".join('\n\n'))
    file1.close()
        
    
# Main function
if __name__ == '__main__':
    questions = nltk.tokenize.sent_tokenize(read_txt_file(os.getcwd()+ "/questions.txt"))
    task1(os.getcwd() + "/Task1_file.txt")
        

   

  
