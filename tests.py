import unittest
from bayes_template import BayesClassifier


class TestClassifier(unittest.TestCase):

    def setUp(self):
        self.bayes = BayesClassifier()
        self.bayes.train()

    def test_pos(self):
        self.assertEqual('positive', self.bayes.classify('I loved the movie.'))

    def test_neg(self):
        self.assertEqual('negative', self.bayes.classify('Ew. Gross. It was nasty. The acting was nasty. :) /sarcasm'))

    def test_newt(self):
        self.assertEqual('neutral', self.bayes.classify('Movies are movies.'))