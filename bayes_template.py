# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re
import json
import json_database


class Bayes_Classifier:
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
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


        # Make two dictionaries each for frequency and presence
        pos_freq = {}
        neg_freq = {}
        pos_pres = {}
        neg_pres = {}

        #for word in total_words:
        #    pos_freq[word] = 0.0
        #    neg_freq[word] = 0.0
        #    pos_pres[word] = 0.0
        #    neg_pres[word] = 0.0

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
            words = text.split(' ')
            if review['status'] == '5':
                pos_word_counter += len(words)
                pos_review_counter += 1
            else:
                neg_word_counter += len(words)
                neg_review_counter += 1

            # Frequency
            if review['status'] == '5':
                for word in words:
                    if word in pos_freq:
                        pos_freq[word] += 1
                    else:
                        pos_freq[word] = 1.0
            else:
                for word in words:
                    if word in neg_freq:
                        neg_freq[word] += 1
                    else:
                        neg_freq[word] = 1.0
            # Presence
            if review['status'] == '5':
                while len(words) > 0:
                    word = words[0]
                    if word in pos_pres:
                        pos_pres[word] += 1
                    else:
                        pos_pres[word] = 1.0
                    while word in words:
                        words.remove(word)
            else:
                while len(words) > 0:
                    word = words[0]
                    if word in neg_pres:
                        neg_pres[word] += 1
                    else:
                        neg_pres[word] = 1.0
                    while word in words:
                        words.remove(word)







        # Normalize the counts after going through all the files
        for a in pos_freq:
            pos_freq[a] /= pos_word_counter
        for a in neg_freq:
            neg_freq[a] /= neg_word_counter
        for a in pos_pres:
            pos_pres[a] /= pos_review_counter
        for a in neg_pres:
            neg_pres[a] /= neg_review_counter



        print 'Positive Frequency:'
        print [pos_freq[i] for i in pos_freq if pos_freq[i] != 0.0]
        print 'Negative Frequency:'
        print [neg_freq[i] for i in neg_freq if neg_freq[i] != 0.0]
        print 'Positive Presence:'
        print [pos_pres[i] for i in pos_pres if pos_pres[i] != 0.0]
        print 'Negative Presence:'
        print [neg_pres[i] for i in neg_pres if neg_pres[i] != 0.0]



    
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """

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