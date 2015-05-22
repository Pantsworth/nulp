# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re, json
import nltk
import json_database
from nltk.tokenize import RegexpTokenizer


class Bayes_Classifier:
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
        self.pos_freq = load_pickle('pos_freq.p')
        self.neg_freq = load_pickle('neg_freq.p')
        self.pos_pres = load_pickle('pos_pres.p')
        self.neg_pres = load_pickle('neg_pres.p')

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""

        if self.pos_freq:
            return

        # Open the database
        # Tokenize each set of text

        total_words = []
        # Go through all positive and negative reviews
        data = json_database.load_json_database()
        #for review in data:
        #    review = json.loads(review)
        #    #print review['text']
        #    for word in review['text'].split(' '):
        #        if word not in total_words:
        #            total_words.append(word)

        #for word in total_words:
        #    self.pos_freq[word] = 0.0
        #    self.neg_freq[word] = 0.0
        #    self.pos_pres[word] = 0.0
        #    self.neg_pres[word] = 0.0

        # Go through all files
        pos_word_counter = 0   #Count the total number of words and documents
        neg_word_counter = 0
        pos_review_counter = 0   #Count the total number of words and documents
        neg_review_counter = 0


        for review in data:
            # get text and store in string
            review = json.loads(review)
            text = review['text']
            #words = self.tokenize(text)
            words = nltk.word_tokenize(text)
            words = [w.lower() for w in words if w.isalpha()]
            # print words
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


        # Normalize the counts after going through all the files
        for a in self.pos_freq:
            self.pos_freq[a] += 1
            self.pos_freq[a] /= (pos_word_counter+1)
        for a in self.neg_freq:
            self.neg_freq[a] += 1
            self.neg_freq[a] /= (neg_word_counter+1)
        for a in self.pos_pres:
            self.pos_pres[a] += 1
            self.pos_pres[a] /= (pos_review_counter+1)
        for a in self.neg_pres:
            self.neg_pres[a] += 1
            self.neg_pres[a] /= (neg_review_counter+1)



        print 'Positive Frequency:'
        print [self.pos_freq[i] for i in self.pos_freq if self.pos_freq[i] != 0.0]
        print 'Negative Frequency:'
        print [self.neg_freq[i] for i in self.neg_freq if self.neg_freq[i] != 0.0]
        print 'Positive Presence:'
        print [self.pos_pres[i] for i in self.pos_pres if self.pos_pres[i] != 0.0]
        print 'Negative Presence:'
        print [self.neg_pres[i] for i in self.neg_pres if self.neg_pres[i] != 0.0]


        save_pickle(self.pos_freq, 'pos_freq.p')
        save_pickle(self.neg_freq, 'neg_freq.p')
        save_pickle(self.pos_pres, 'pos_pres.p')
        save_pickle(self.neg_pres, 'neg_pres.p')

        return 1

    
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        # self.pos_pres is number of pos documents that contain given word divided by number of pos documents
        # self.pos_freq =number of times a word appears in all the positive documents divided by total words in pos docs
        # take in text, tokenize it
        # check how likely words used are to be positive
        # check how likely it is words used are negative

        word_tokens = nltk.word_tokenize(sText)
        word_tokens = [w.lower() for w in word_tokens if w.isalpha()]

        tokens_length = len(word_tokens)
        pos_sum = 0
        neg_sum = 0
        pos_miss = 0
        neg_miss = 0

        for token in word_tokens:
            try:
                pos_sum += -(math.log10(self.pos_pres[token]))
            except KeyError:
                pos_miss += 1
                print token, pos_miss
            try:
                neg_sum += -(math.log10(self.neg_pres[token]))
            except KeyError:
                neg_miss += 1
                print token, neg_miss

        print pos_sum, neg_sum

        pos_sum *= (1.0*(tokens_length-pos_miss)/tokens_length)
        neg_sum *= (1.0*(tokens_length-neg_miss)/tokens_length)


        print pos_sum, neg_sum


    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt
   
    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()
   
    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText):
        """Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))
               
        if sToken != "":
            lTokens.append(sToken)

        return lTokens


def freed_tokenize(sText):
      """Given a string of text sText, returns a list of the individual tokens that
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))

      if sToken != "":
         lTokens.append(sToken)

      return lTokens


def load_pickle(filename):
    model_file = relative_path(filename)
    if os.path.isfile(model_file):
        return pickle.load(open(model_file, 'rb'))
    return {}


def save_pickle(object, filename):
    model_file = open(relative_path(filename), 'wb')
    pickle.dump(object, model_file)
    model_file.close()


def relative_path(path):
    """
    Get file path relative to calling script's directory
    :param path: filename or file path
    :return: full path name, relative to script location
    """
    return os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), path)
