from flask_philo import app
from app.analytics.predictors import MeanPredictoRunner
from prettytable import PrettyTable

import argparse
import os
import uuid


def run(**kwargs):
    """
    KFold experiment Mean Predictor
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--kn', help='Number of Folds', required=False,
        default=None, type=int)
    parser.add_argument(
        '--t', help='threshold ', required=False, default=2, type=int)

    args, extra_params = parser.parse_known_args()
    runner = MeanPredictoRunner(kn=args.kn, threshold=args.t)

    t = PrettyTable([
        'Predictor',
        'Number of K-folds', 'Threshold', 'Coverage', 'RMSE',
        'Total Execution Time (Minutes)'

    ])

    if args.kn is None:
        kn = 'Leave One Out'
    else:
        kn = args.kn

    t.add_row([
        'Mean Predictor',
        kn, args.t, '{0:.3g}'.format(runner.evaluator.coverage),
        '{0:.3g}'.format(runner.evaluator.rmse),
        runner.total_execution_time
    ])
    print(t)

    fname = os.path.join(
        app.config['DATA_DIR'], 'results', 'MeanPredictor_{}.txt'.format(
            str(uuid.uuid4()).split('-')[0]))

    with open(fname, 'w') as f:
        f.write(str(t))
