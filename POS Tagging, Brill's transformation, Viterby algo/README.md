Brill's, viterbi, naive bayes are seperate folders

To run brill's algorithm:
- open Brill's folder
- run py test.py <test sentence>
- Outputs given are:
	> brillsTagging-OUTPUT: birll's tag for each word in test sentence
	> brillsTags : Previous, from and to tags and each of their transition scores
	> mostProbable-OPTPUT: most probable tag for each word in test sentence
	> mostPrabableTags : most probable tag for each word in corpus

To run Naive bayes algorithm: 
- open Naive Bayes folder
- run py NBtagging.py
- Program will prompt user to enter training data file path
- Program will prompt use to enter test sentence
- Naive Bayes tagging for each word will be given as output

To run viterby algorithm:
- open viterbi folder
- run py Viterbi.py
- Program will prompt user to enter the test sentence
- Outputs given are:
	> Probability for the observation sequence
	> Most likely Tag sequence