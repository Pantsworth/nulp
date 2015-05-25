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
    false_positive = 0.0
    false_negative = 0.0
    true_positive = 0.0
    for review in test_data:
        if review['status'] == '5':
            result = 'positive'
        else:
            result = 'negative'

        if classifier.classify(review['text']) != result:
            if result == 'positive':
                false_negative += 1
            else:
                false_positive += 1
        elif result == 'positive':
            true_positive += 1
    precision = true_positive/(true_positive+false_positive)
    recall = true_positive/(true_positive+false_negative)
    f = 2.0*precision*recall/(precision+recall)
    return precision, recall, f

if __name__ == '__main__':
    main()
