import unittest
import bayes
import bayesbest


class TestClassifier(unittest.TestCase):

    def setUp(self):
        self.bayes = bayes.BayesClassifier()
        self.bayes.train()

    def test_pos(self):
        self.assertEqual('positive', self.bayes.classify('I loved the movie.'))

    def test_neg(self):
        self.assertEqual('negative', self.bayes.classify('Ew. Gross. It was nasty. The acting was nasty. :) /sarcasm'))

    def test_newt(self):
        self.assertEqual('neutral', self.bayes.classify('Movies are movies.'))


class TestBest(unittest.TestCase):

    def setUp(self):
        self.bayes = bayesbest.BayesClassifier()
        self.bayes.train()

    def test_pos(self):
        self.assertEqual('positive', self.bayes.classify('I loved the movie.'))

    def test_neg(self):
        self.assertEqual('negative', self.bayes.classify('Ew. Gross. It was nasty. The acting was nasty. :) /sarcasm'))

    def test_newt(self):
        self.assertEqual('neutral', self.bayes.classify('Movies are movies.'))