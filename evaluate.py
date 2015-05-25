from random import shuffle
import json
import bayesbest
import bayes
import itertools


def segment_corpus(corpus, fold):
    """
    Given a corpus, segment it into a number of sub-corpora
    :param corpus: object containing data
    :param fold: number of segments
    :return: array of data objects with size fold
    """

    shuffle(corpus)
    splitted = fold*[[]]
    for i, obj in enumerate(corpus):
        splitted[i % 10].append(obj)
    return splitted


def main():
    fold = 10
    with open(bayesbest.relative_path('data.json'), 'r') as f:
        corpus = json.load(f)
    sub_corpora = segment_corpus(corpus, fold)
    for i in range(fold):
        print "Running subsection %x of %x" % (i, fold)
        print "  bayes:"
        run_evaluation(itertools.chain(sub_corpora[:i]+sub_corpora[i+1:]), sub_corpora[i], bayes.BayesClassifier())
        print "  bayesbest:"
        run_evaluation(itertools.chain(sub_corpora[:i]+sub_corpora[i+1:]), sub_corpora[i], bayesbest.BayesClassifier())


def run_evaluation(training_data, test_data, classifier):

    classifier.train(training_data)
    for review in test_data:
        

    pass


if __name__ == '__main__':
    main()
