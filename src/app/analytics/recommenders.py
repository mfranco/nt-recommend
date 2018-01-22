from app.qa.evaluators import RecommenderEvaluator
from app.recommenders import (
    FrequentItemRecommender, LinkedItemRecommender, PredictorRecommender
)
from flask_philo import app
import os


class FrequentItemRecommenderRunner(object):
    def __init__(
            self, kn=None, neighbourhood_size=10, similarity_metric='msd'):
        db_dir = os.path.join(
            app.config['DATA_DIR'], 'db', 'ml-latest-small')

        init_recommender_params = {
            'neighbourhood_size': neighbourhood_size,
            'similarity_metric': similarity_metric
        }
        app.logger.info('Starting FrequentItemRecommender Evaluator')
        self.evaluator = RecommenderEvaluator(
            db_dir, recommender_class=FrequentItemRecommender,
            init_recommender_params=init_recommender_params, n_splits=kn)
        self.evaluator.run()
        self.total_execution_time = self.evaluator.total_execution_time


class LinkedItemRecommenderRunner(object):
    def __init__(
            self, kn=None, neighbourhood_size=10, similarity_metric='msd'):
        db_dir = os.path.join(
            app.config['DATA_DIR'], 'db', 'ml-latest-small')

        init_recommender_params = {
            'neighbourhood_size': neighbourhood_size,
            'similarity_metric': similarity_metric
        }
        app.logger.info('Starting LinkedItemRecommender Evaluator')
        self.evaluator = RecommenderEvaluator(
            db_dir, recommender_class=LinkedItemRecommender,
            init_recommender_params=init_recommender_params, n_splits=kn)
        self.evaluator.run()
        self.total_execution_time = self.evaluator.total_execution_time


class MeanPredictorRecommenderRunner(object):
    def __init__(
            self, kn=None, neighbourhood_size=10, similarity_metric='msd'):

        db_dir = os.path.join(
            app.config['DATA_DIR'], 'db', 'ml-latest-small')

        init_recommender_params = {
            'neighbourhood_size': neighbourhood_size, 'predictor_name': 'mean',
            'similarity_metric': similarity_metric
        }

        app.logger.info('Starting MeanPredictorRecommender Evaluator')
        self.evaluator = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params, n_splits=kn)
        self.evaluator.run()
        self.total_execution_time = self.evaluator.total_execution_time


class CollaborativePredictorRecommenderRunner(object):
    def __init__(
            self, kn=None, neighbourhood_size=10, similarity_metric='msd'):
        db_dir = os.path.join(
            app.config['DATA_DIR'], 'db', 'ml-latest-small')

        init_recommender_params = {
            'neighbourhood_size': neighbourhood_size,
            'predictor_name': 'collaborative',
            'similarity_metric': similarity_metric
        }

        app.logger.info('Starting CollaborativePredictorRecommender Evaluator')
        self.evaluator = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params, n_splits=kn)
        self.evaluator.run()
        self.total_execution_time = self.evaluator.total_execution_time


class ResnikPredictorRecommenderRunner(object):
    def __init__(
            self, kn=None, neighbourhood_size=10, similarity_metric='msd'):
        db_dir = os.path.join(
            app.config['DATA_DIR'], 'db', 'ml-latest-small')

        init_recommender_params = {
            'neighbourhood_size': neighbourhood_size,
            'predictor_name': 'resnik',
            'similarity_metric': similarity_metric
        }

        app.logger.info('Starting ResnikPredictorRecommender Evaluator')
        self.evaluator = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params, n_splits=kn)
        self.evaluator.run()
        self.total_execution_time = self.evaluator.total_execution_time
