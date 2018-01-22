from flask_philo import app
from app.analytics.recommenders import LinkedItemRecommenderRunner
from prettytable import PrettyTable

import argparse
import os
import uuid


def run(**kwargs):
    """
    KFold experiment for LinkedItemRecommenderRunner
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--kn', help='Number of Folds', required=False, default=None, type=int)

    parser.add_argument(
        '--ns', help='Neigbourhood size', required=False, default=10, type=int)

    parser.add_argument(
        '--m', help='similarity metric ', required=True,
        choices=('cosine', 'euclidean', 'msd', 'pearson'))

    args, extra_params = parser.parse_known_args()

    runner = LinkedItemRecommenderRunner(
        kn=args.kn, neighbourhood_size=args.ns, similarity_metric=args.m)

    t = PrettyTable([
        'Recommender',
        'Number of K-folds', 'Neigbourhood size', 'Similarity Metric',
        'Precision', 'Recall', 'F1', 'Total Execution Time (Minutes)'

    ])

    if args.kn is None:
        kn = 'Leave One Out'
    else:
        kn = args.kn

    t.add_row([
        'LinkedItemRecommenderRecommender',
        kn, args.ns, args.m, '{0:.3g}'.format(runner.evaluator.precision),
        '{0:.3g}'.format(runner.evaluator.recall),
        '{0:.3g}'.format(runner.evaluator.f1),
        runner.total_execution_time
    ])
    print(t)

    fname = os.path.join(
        app.config['DATA_DIR'], 'results', 'LinkedItemRecommender_{}.txt'.format(
            str(uuid.uuid4()).split('-')[0]))

    with open(fname, 'w') as f:
        f.write(str(t))
