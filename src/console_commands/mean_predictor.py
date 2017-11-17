from app.analytics.predictors import MeanPredictoRunner
from prettytable import PrettyTable
import argparse


def run(**kwargs):
    """
    KFold experiment Mean Predictor
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--kn', help='Number of Folds', required=False, default=None)
    parser.add_argument(
        '--t', help='threshold ', required=False, default=2, type=int)

    args, extra_params = parser.parse_known_args()
    runner = MeanPredictoRunner(kn=args.kn, threshold=args.t)

    t = PrettyTable([
       'Number of K-folds', 'Threshold', 'Coverage', 'RMSE'

    ])

    t.add_row([
        args.kn, args.t, '{0:.3g}'.format(runner.evaluator.coverage),
        '{0:.3g}'.format(runner.evaluator.rmse)
    ])
    print(t)
