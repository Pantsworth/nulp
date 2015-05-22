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
        bayes.classify("the")





class TestDatabase(unittest.TestCase):

    def testOutput(self):
        json_data = json_database.load_json_database()

