
import pandas as pd
import numpy as np



transitionProb = pd.read_csv('Transition_Probabilities.csv')
transitionProb.set_index('Tags', inplace=True)

observationProb = pd.read_csv('Observation_Probabilities.csv')
observationProb.set_index('Tags', inplace=True)

states = transitionProb.columns

input_sentence = input("Enter sentence : ")
observedSequence = input_sentence.strip().split()
observedSequence.insert(0, '<s>')


def hMM_ViterbiDecodingAlgorithm(observedSequence):
    viterbiTable = []
    startState = 0
    for word in observedSequence[1:]:
        trellis = []
        for tag in states:
            if startState == 0:
                trellis.append(([transitionProb.loc[observedSequence[0]][tag] * observationProb.loc[tag][word], -1, observedSequence[0], tag, word]))
            else:
                maxProbVal = -1
                currState = []
                for index, prev_state in enumerate(viterbiTable[-1]):
                    currProbVal = prev_state[0] * transitionProb.loc[states[index]][tag] * observationProb.loc[tag][word]
                    if currProbVal > maxProbVal:
                        maxProbVal = currProbVal
                        currState = [currProbVal, index, states[index], tag, word]
                trellis.append(currState)
        startState += 1
        viterbiTable.append(trellis)


    maxIndexProb = np.argmax([lastSubRow[0] for lastSubRow in viterbiTable[-1]])
    sequence_probability = viterbiTable[-1][maxIndexProb][0]
    tagSequence = []

    for eachObservStates in reversed(viterbiTable):
        tagSequence.append(eachObservStates[maxIndexProb][4] + '_' + eachObservStates[maxIndexProb][3])
        maxIndexProb = eachObservStates[maxIndexProb][1]
    tagSequence = tagSequence[::-1]
    return sequence_probability, tagSequence


tagSeqProb, tagSequence = hMM_ViterbiDecodingAlgorithm(observedSequence)
print("Probability for the Observation sequence : " + str(tagSeqProb))
print("Most likely Tag Sequence : " + str(tagSequence))

