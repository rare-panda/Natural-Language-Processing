Bigram Probabilities
	a. Write a computer program to compute the bigram model (counts and probabilities) on 
	   the given corpus (NLP6320_POSTaggedTrainingSet.txt) provided as Addendum to 
	   this homework on eLearning) under the following three (3) scenarios:
		i. No Smoothing
		ii. Add-one Smoothing
		iii. Good-Turing Discounting based Smoothing
	   		Note: Please the set the Good Turing smoothed count C*_(c)=0 if N_(c+1)=0
	   Note: Smoothing performed only for the bigram model.
	b. Write a computer program to compute the bigram based probability of any input test 
	   sentence using the above trained model(s) 
		Note: 
		a. Your program should accept one of the above specified smoothing “type” 
		as an input argument.
		b. Smoothing performed only for the bigram model.
Other Instructions:
	1. Use each line (ending with newline character) in the corpus as a single text 
	   sentence.
	2. Use whitespace (i.e. space, tab, and newline) to tokenize each text sentence
	   words/tokens that are required for the unigram and bigram model.
	3. Use the WORD_POS pattern to extract the actual word (i.e. the WORD part 
	   in the WORD_POS pattern) from the tokenized word.
	   For example, in the tokenized word “Brainpower_NNP”, “Brainpower” is the 
	   WORD and “NNP” is the POS. Use “Brainpower” as the actual word/token 
	   for the unigram and bigram creation.
	4. The bigrams should be created ONLY within each text sentence and 
	   computed for the entire corpus.
	5. Convert all words/tokens to lowercase. Do NOT perform any other type of 
	   word/token normalization (i.e. stem, lemmatize, etc.). 
	6. Creation and matching of unigrams and bigrams should be exact and caseinsensitive. 
	7. Please do not submit the unigram and bigram models (counts and 
	   probabilities) with the homework solution submission. The TA can run your 
	   program to produce and check the unigram and bigram models
How to run the python file:
	- Run the file program.py
	- The program then prompts for training corpus file location.
	- It generates three probabilities of No Smoothing, Add One and Good Turing for the corpus in the form of txt files that are stored in the same location as the python file.
	- The program the prompts the user to input test a sentence and the smoothing technique. Please provide both upon running. 
	- The program prints the probability of the given sentence with the given technique.
