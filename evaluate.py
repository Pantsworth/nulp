import json
import bayesbest
import itertools

def segment_corpus(corpus, fold):
    """
    Given a corpus, segment it into a number of sub-corpora
    :param corpus: object containing data
    :param fold: number of segments
    :return: array of data objects with size fold
    """
    pass


def main():
    fold = 10
    with open(bayesbest.relative_path('data.json'), 'r') as f:
        corpus = json.load(f)
    sub_corpora = segment_corpus(corpus, fold)
    for i in range(fold):
        run_evaluation(itertools.chain(sub_corpora[:i]+sub_corpora[i:]), sub_corpora[i])


def run_evaluation(training_data, test_data):
    pass


if __name__ == '__main__':
    main()
