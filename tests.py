__author__ = 'DoctorWatson'
import unittest
import json_database
import json
from bayes_template import Bayes_Classifier

class TestClassifier(unittest.TestCase):

    def test_something(self):
        self.assertEqual(1, 1)

    def test_train(self):
        bayes = Bayes_Classifier()
        Bayes_Classifier.train(bayes)
        # bayes.classify("Unstoppable and righteous, it roars across the no-lane hardpan like the four-iron horseman of "
        #                "the kinetic apocalypse, amped up on bathtub crank and undiluted movie love. Oh, what a movie. "
        #                "What a lovely movie!")
        bayes.classify("I love this film")

class TestDatabase(unittest.TestCase):

    def testOutput(self):
        json_data = json_database.load_json_database()

