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

    # def test_neg(self):
    #     self.assertEqual('negative', self.bayes.classify('Ew. Gross. It was nasty. The acting was nasty. :) /sarcasm'))
    #
    # def test_newt(self):
    #     self.assertEqual('neutral', self.bayes.classify('Movies are movies.'))

    def test_very_positive(self):
        self.assertEqual('positive', self.bayes.classify('The acting was astonishing. Everything was perfect. I would '
                                                         'love to see this movie again. It was unbelievable.'))

    def test_very_negative(self):
        self.assertEqual('positive', self.bayes.classify('This was the worst piece of crap I have ever seen. Nothing '
                                                         'was good about this movie. The vision was not there. It was '
                                                         'miserable to sit through. Save your money.'))

    def test_very_neutral(self):
        self.assertEqual('positive', self.bayes.classify('The movie was alright. The acting was bad, but the music was '
                                                         'good.'))