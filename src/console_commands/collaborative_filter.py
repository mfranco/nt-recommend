from flask_philo import app
from app.analytics.predictors import CollaborativePredictoRunner
from prettytable import PrettyTable

import argparse
import os
import uuid


def run(**kwargs):
    """
    KFold experiment for Collaborative Filtering
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--t', help='threshold ', required=False, default=1, type=int)

    parser.add_argument(
        '--kn', help='Number of Folds', required=False, default=None)

    parser.add_argument(
        '--m', help='similarity metric ', required=True)

    parser.add_argument(
        '--ns', help='neighbourhood size ', required=True, type=int)

    args, extra_params = parser.parse_known_args()

    sim = ('cosine', 'euclidean', 'msd', 'pearson')
    if args.m not in sim:
        print('\n Invalid similarity metric, valid values are: \n')
        for s in sim:
            print(s)
            print('\n')
        exit(1)

    runner = CollaborativePredictoRunner(
        kn=args.kn, similarity_metric=args.m, neighbourhood_size=args.ns,
        threshold=args.t)

    t = PrettyTable([
       'Number of K-folds', 'Threshold', 'Coverage', 'RMSE',
       'Total Execution Time (Minutes)'

    ])

    t.add_row([
        args.kn, args.t, '{0:.3g}'.format(runner.evaluator.coverage),
        '{0:.3g}'.format(runner.evaluator.rmse),
        runner.total_execution_time
    ])
    print(t)

    fname = os.path.join(
        app.config['DATA_DIR'], 'results', '{}.txt'.format(
        str(uuid.uuid4()).split('-')[0]))

    with open(fname, 'w') as f:
        f.write(str(t))
