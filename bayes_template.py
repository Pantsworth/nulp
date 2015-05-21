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
        for review in data:
            review = json.loads(review)
            #print review['text']
            for word in review['text'].split(' '):
                if word not in total_words:
                    total_words.append(word)


        # Make two dictionaries each for frequency and presence
        pos_freq = {}
        neg_freq = {}
        pos_pres = {}
        neg_pres = {}
        pos_words = []

        for word in total_words:
            pos_freq[word] = 0.0
            neg_freq[word] = 0.0
            pos_pres[word] = 0.0
            neg_pres[word] = 0.0

        # Go through all files
        for review in data:
            # get text and store in string
            review = json.loads(review)
            text = review['text']
            #words = self.tokenize(text)
            words = text.split(' ')

            # Frequency
            if review['status'] == 5:
                for word in words:
                    pos_freq[word] += 1
            else:
                for word in words:
                    neg_freq[word] += 1

            # Presence

            #for (word, freq) in pos_words:
            
            if review['status'] == 5:
                for word in total_words:
                    if word in words:
                        pos_pres[word] += 1
            else:
                for word in total_words:
                    if word in words:
                        pos_pres[word] += 1

        print pos_freq
        print neg_freq
        print pos_pres
        print neg_pres

        # After going through all the files





    
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