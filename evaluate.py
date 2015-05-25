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
    splitted = []
    for i in range(fold):
        splitted.append([])
    for i, obj in enumerate(corpus):
        splitted[i % 10].append(obj)
    return splitted


def main():
    fold = 10
    with open(bayesbest.relative_path('data.json'), 'r') as f:
        corpus = json.load(f)
    sub_corpora = segment_corpus(corpus, fold)
    p1 = 0
    r1 = 0
    f1 = 0
    p2 = 0
    r2 = 0
    f2 = 0
    for i in range(fold):
        print "Running subsection", str(i+1), "of", str(fold)
        _p1, _r1, _f1 = run_evaluation(itertools.chain.from_iterable(sub_corpora[:i]+sub_corpora[i+1:]), sub_corpora[i],
                                       bayes.BayesClassifier())
        print '  ', _p1, _r1, _f1
        _p2, _r2, _f2 = run_evaluation(itertools.chain.from_iterable(sub_corpora[:i]+sub_corpora[i+1:]), sub_corpora[i],
                                       bayesbest.BayesClassifier())
        print '  ', _p2, _r2, _f2
        p1 += _p1
        r1 += _r1
        f1 += _f1
        p2 += _p2
        r2 += _r2
        f2 += _f2
    p1 /= fold
    r1 /= fold
    f1 /= fold
    p2 /= fold
    r2 /= fold
    f2 /= fold
    print "Averages:"
    print '  ', p1, r1, f1
    print '  ', p2, r2, f2


def run_evaluation(training_data, test_data, classifier):
    print '  training...'
    classifier.train(training_data)
    print '  classifying...'
    false_positive = 0.0
    false_negative = 0.0
    true_positive = 0.0
    for review in test_data:
        review = json.loads(review)
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
