# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #

    # Read training data

    states = dict()
    idx_to_states = dict()
    observations = dict()
    tag_ps = dict()

    train_words = []
    train_labels = []
    test_words = []

    for i in training_list:
        file = open(i, "r")

        for line in file:
            x = line.split(" : ")
            word = x[0]
            label = x[1].split("\n")[0]
            train_words.append(word)
            train_labels.append(label)

            if word not in observations:
                observations[word] = len(observations)

            if label not in states:
                idx = len(states)
                states[label] = idx
                idx_to_states[idx] = label

            if label not in tag_ps:
                tag_ps[label] = 1
            else:
                tag_ps[label] += 1

        file.close()

    tag_values = list(tag_ps.values())
    tag_probs = np.array(tag_values).reshape((len(tag_values),-1))

    file = open(test_file, "r")
    for w in file:
        word = w.split("\n")[0]
        test_words.append(word)
        if word not in observations:
            observations[word] = len(observations)

    file.close()

    train_words_s, train_labels_s = split_sentence(train_words,train_labels)
    test_words_s = split_sentence(test_words,None)

    num_train_sentences = len(train_words_s)
    num_test_sentences = len(test_words_s)

    transition_ps = np.zeros((len(states),len(states)))
    emission_ps = np.zeros((len(states),len(observations)))
    initial_ps = np.zeros(len(states))

    last_label = None

    for i in range(0,num_train_sentences):

        word_sentence = train_words_s[i]
        label_sentence = train_labels_s[i]

        for j in range(0,len(word_sentence)):
            word = word_sentence[j]
            label = label_sentence[j]

            if j == 0:
                initial_ps[states[label]] += 1
                last_label = None

            if last_label is not None:
                transition_ps[states[last_label],states[label]] += 1

            emission_ps[states[label],observations[word]] += 1

            last_label = label

    for i in range(0,num_test_sentences):

        word_sentence = test_words_s[i]

        for j in range(0,len(word_sentence)):
            word = word_sentence[j]

            if word not in train_words:
                emission_ps[:,observations[word]] = np.squeeze(tag_probs)

    initial_ps = np.divide(initial_ps, np.sum(initial_ps, axis=0))
    transition_ps = np.divide(transition_ps, np.sum(transition_ps, axis=0))
    emission_ps = np.divide(emission_ps, np.sum(emission_ps, axis=1).reshape(-1,1))

    S = states.keys()

    test_labels = []

    for O in test_words_s:

        prob_trellis, path_trellis = Viterbi(S,O,initial_ps,transition_ps,emission_ps,observations)

        previous_label_val = np.argmax(prob_trellis[:,len(O)-1])
        previous_label = idx_to_states[previous_label_val]


        test_sentence_labels = [previous_label]

        for i in range(len(O)-1,0,-1):

            previous_label_val = path_trellis[previous_label_val,i]
            previous_label = idx_to_states[previous_label_val]
            test_sentence_labels = [previous_label] + test_sentence_labels

        test_labels = test_labels + test_sentence_labels
    
    out_file = open(str(output_file), "w")
    for i in range(0,len(test_words)):
        out_file.write(str(test_words[i]) + " : " + str(test_labels[i]) + "\n")

    out_file.close()

    return

def Viterbi(S, O, initial_ps, transition_ps, emission_ps, observations):

    S = list(S)
    O = list(O)

    observations = dict(observations)

    prob_trellis = np.zeros((len(S), len(O)))
    path_trellis = np.full((len(S), len(O)), -1)

    prob_trellis[:,0] = np.multiply(initial_ps,emission_ps[:,observations[O[0]]])
    prob_trellis[:,0] = np.divide(prob_trellis[:,0], sum(prob_trellis[:,0]))

    for o in range(1,len(O)):
        inter_1 = np.multiply(transition_ps,prob_trellis[:,o-1].reshape(-1,1))
        inter_2 = np.multiply(inter_1,emission_ps[:,observations[O[o]]].reshape(-1,1).T)
        inter_3 = np.amax(inter_2, axis=0) #most likely probability to get to new state
        inter_4 = np.argmax(inter_2, axis=0) #most likely old state to get to new state

        prob_trellis[:,o] = np.divide(inter_3, np.sum(inter_3))
        path_trellis[:,o] = inter_4

    return prob_trellis, path_trellis

def split_sentence(words,labels):

    words = list(words)

    if labels is None:

        words_split = []

        end_sentence = False
        quote_detected = False
        new_word_sentence = []

        for i in range(0, len(words)):

            word = words[i]

            if (word == "." or word == "?" or word == "!") and not quote_detected:
                end_sentence = True

            if word == "\"" and not quote_detected:
                quote_detected = True

            if word == "\"" and quote_detected:
                quote_detected = False
                end_sentence = True

            new_word_sentence.append(word)

            if end_sentence:
                words_split.append(new_word_sentence)
                new_word_sentence = []
                end_sentence = False

        return words_split

    else:

        labels = list(labels)

        words_split = []
        labels_split = []

        end_sentence = False
        quote_detected = False

        new_word_sentence = []
        new_label_sentence = []

        for i in range(0, len(words)):
            word = words[i]
            label = labels[i]

            if (word == "." or word == "?" or word == "!") and not quote_detected:
                end_sentence = True

            if word == "\"" and not quote_detected:
                quote_detected = True

            if word == "\"" and quote_detected:
                quote_detected = False
                end_sentence = True

            new_word_sentence.append(word)
            new_label_sentence.append(label)

            if end_sentence:
                words_split.append(new_word_sentence)
                labels_split.append(new_label_sentence)
                new_word_sentence = []
                new_label_sentence = []
                end_sentence = False

        return words_split, labels_split

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d") + 1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t") + 1]
    output_file = parameters[parameters.index("-o") + 1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag(training_list, test_file, output_file)