__author__ = 'DoctorWatson'
import unittest
import json_database
import json
from bayes_template import Bayes_Classifier
import math

class TestClassifier(unittest.TestCase):

    def setUp(cls):
        cls.bayes = Bayes_Classifier()
        cls.bayes.train()

    def test_train(self):
        bayes = Bayes_Classifier()
        Bayes_Classifier.train(bayes)
        # bayes.classify("Unstoppable and righteous, it roars across the no-lane hardpan like the four-iron horseman of "
        #                "the kinetic apocalypse, amped up on bathtub crank and undiluted movie love. Oh, what a movie. "
        #                "What a lovely movie!")
        bayes.classify("It was definitely a movie.")
        print math.log10(bayes.pos_pres["loved"])
        print math.log10(bayes.neg_pres["loved"])

    def test_pos(self):
        self.assertEqual('positive', self.bayes.classify('I loved the movie.'))

    def test_neg(self):
        self.assertEqual('negative', self.bayes.classify('Ew. Gross. It was nasty. The acting was nasty. :) /sarcasm'))

    def test_newt(self):
        self.assertEqual('neutral', self.bayes.classify('Movies are movies.'))


class TestDatabase(unittest.TestCase):

    def testOutput(self):
        json_data = json_database.load_json_database()

