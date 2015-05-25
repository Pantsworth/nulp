# Name: Michael Nowakowski (mjn912), Adam Snyder (ars123) and Steven Vorbrich (slv398)
# Date: 24 May 2015
# Description: Naive Bayes Classifier
#
#

import math
import os
import pickle
import json
import nltk
import json_database


class BayesClassifier:
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""

        self.pos_freq = load_pickle('pos_freq.p')
        self.neg_freq = load_pickle('neg_freq.p')
        self.pos_pres = load_pickle('pos_pres.p')
        self.neg_pres = load_pickle('neg_pres.p')

    def train(self, training_data=()):
        """Trains the Naive Bayes Sentiment Classifier."""

        # Open the database
        if training_data:
            data = training_data
        else:
            # If we have pickle files, there is no need to train
            if self.pos_pres and self.neg_pres:
                return 1
            data = json_database.load_json_database()

        # Initialize counters for words and documents
        pos_word_counter = 0
        neg_word_counter = 0
        pos_review_counter = 0
        neg_review_counter = 0

        for review in data:
            # Get text and store in string
            if not training_data:
                review = json.loads(review)
            print '123'
            if training_data:
                print review
            words = [word.lower() for word in nltk.word_tokenize(review['text'])]

            # Increment counters
            if review['status'] == '5':
                pos_word_counter += len(words)
                pos_review_counter += 1
            else:
                neg_word_counter += len(words)
                neg_review_counter += 1

            # Frequency
            if review['status'] == '5':
                for word in words:
                    if word in self.pos_freq:
                        self.pos_freq[word] += 1
                    else:
                        self.pos_freq[word] = 1.0
            else:
                for word in words:
                    if word in self.neg_freq:
                        self.neg_freq[word] += 1
                    else:
                        self.neg_freq[word] = 1.0

            # Presence
            if review['status'] == '5':
                while len(words) > 0:
                    word = words[0]
                    if word in self.pos_pres:
                        self.pos_pres[word] += 1
                    else:
                        self.pos_pres[word] = 1.0
                    while word in words:
                        words.remove(word)
            else:
                while len(words) > 0:
                    word = words[0]
                    if word in self.neg_pres:
                        self.neg_pres[word] += 1
                    else:
                        self.neg_pres[word] = 1.0
                    while word in words:
                        words.remove(word)

        # Normalize the counts after going through all the files and apply add-one smoothing
        for a in self.pos_freq:
            self.pos_freq[a] += 1
            self.pos_freq[a] /= (pos_word_counter+len(self.pos_pres))
        for a in self.neg_freq:
            self.neg_freq[a] += 1
            self.neg_freq[a] /= (neg_word_counter+len(self.neg_pres))
        for a in self.pos_pres:
            self.pos_pres[a] += 1
            self.pos_pres[a] /= (pos_review_counter+len(self.pos_pres))
        for a in self.neg_pres:
            self.neg_pres[a] += 1
            self.neg_pres[a] /= (neg_review_counter+len(self.neg_pres))

        # Save the training data with pickle
        save_pickle(self.pos_freq, 'pos_freq.p')
        save_pickle(self.neg_freq, 'neg_freq.p')
        save_pickle(self.pos_pres, 'pos_pres.p')
        save_pickle(self.neg_pres, 'neg_pres.p')

        return 1
    
    def classify(self, s_text):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        # self.pos_pres: number of pos documents that contain given word divided by number of pos documents
        # self.pos_freq: number of times a word appears in all the positive documents divided by total words in pos docs
        # take in text, tokenize it
        # check how likely words used are to be positive
        # check how likely it is words used are negative

        words = [word.lower() for word in nltk.word_tokenize(s_text)]

        # Initialize probabilities to 0
        pos_sum = 0
        neg_sum = 0

        # Add the logs of the probabilities (an alternative to multiplying the probabilities)
        for token in words:
            try:
                pos_sum += (math.log10(self.pos_pres[token]))
                neg_sum += (math.log10(self.neg_pres[token]))
            except KeyError:
                pass  # The word was not in our training data, so we ignore it

        # Declare the sentiment
        if abs(pos_sum-neg_sum) < 1.5:
            return 'neutral'
        if pos_sum > neg_sum:
            return 'positive'
        else:
            return 'negative'


# Custom helper functions:

def load_pickle(filename):
    """
    Load a pickle and return the object
    :param filename: File path for desired pickle
    :return: Object
    """
    model_file = relative_path(filename)
    if os.path.isfile(model_file):
        return pickle.load(open(model_file, 'rb'))
    return {}


def save_pickle(object_to_save, filename):
    """
    Save an object as a pickle file
    :param object_to_save: Object to save
    :param filename: File destination
    """
    model_file = open(relative_path(filename), 'wb')
    pickle.dump(object_to_save, model_file)
    model_file.close()


def relative_path(path):
    """
    Get file path relative to calling script's directory
    :param path: filename or file path
    :return: full path name, relative to script location
    """
    return os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), path)
