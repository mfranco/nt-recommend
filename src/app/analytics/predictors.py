from app.qa.evaluators import PredictorEvaluator
from app.predictors.mean_predictor import MeanPredictor
from app.predictors.collaborative import (
    CollaborativePredictor, ResnickPredictor)
from flask_philo import app


import os


class MeanPredictoRunner(object):
    """
    Runs benchmark for Mean Predictor
    """
    def __init__(self, kn=None, threshold=2):
        dir_name = os.path.join(
            app.config['DATA_DIR'], 'db', 'ml-latest-small')
        predictor_params = {'threshold': threshold}
        app.logger.info('Starting MeanPredictor Evaluator')
        if kn is not None:
            kn = int(kn)
        self.evaluator = PredictorEvaluator(dir_name, MeanPredictor, n_splits=kn)
        predictor_params=predictor_params
        app.logger.info('Running MeanPredictor Evaluator')
        self.evaluator.run(predictor_params=predictor_params)


class CollaborativePredictoRunner(object):
    """
    Runs benchmark for Collaborative Filtering
    """
    def __init__(
            self, kn=None, similarity_metric='msd',
            neighbourhood_size=100, threshold=1, predictor_class='collaborative'):
        dir_name = os.path.join(
            app.config['DATA_DIR'], 'db', 'ml-latest-small')
        app.logger.info('Starting CollaborativePredictor Evaluator')

        if kn is not None:
            kn = int(kn)

        predictor_ditc = {
            'collaborative': CollaborativePredictor,
            'resnik': ResnickPredictor
        }

        predictor_params = {
            'threshold': threshold,
            'neighbourhood_size': neighbourhood_size,
            'similarity_metric': similarity_metric
        }

        self.evaluator = PredictorEvaluator(
            dir_name, predictor_ditc[predictor_class],
            n_splits=kn, predictor_params=predictor_params)

        app.logger.info('Running CollaborativePredictor Evaluator')
        self.evaluator.run()
