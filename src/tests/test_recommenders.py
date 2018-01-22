from app.models import DB
from app.qa.evaluators import RecommenderEvaluator
from app.recommenders import (
    FrequentItemRecommender, LinkedItemRecommender, PredictorRecommender
)
from flask_philo.test import FlaskTestCase

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestRecommenders(FlaskTestCase):
    def setup(self):
        db_dir = os.path.join(BASE_DIR, 'data', 'recommenders')
        self.db = DB(db_dir=db_dir)

    def test_frequent_item_recommender(self):
        recommender = FrequentItemRecommender(self.db)
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)

    def test_linked_item_recommender(self):
        recommender = LinkedItemRecommender(self.db)
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)

    def test_mean_predictor_recommender(self):
        recommender = PredictorRecommender(self.db, predictor_name='mean')
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)

    def test_collaborative_predictor_recommender(self):
        recommender = PredictorRecommender(self.db, predictor_name='collaborative')
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)

    def test_resnik_predictor_recommender(self):
        recommender = PredictorRecommender(self.db, predictor_name='resnik')
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)


class TestEvaluator(FlaskTestCase):

    def test_frequent_item_recommender(self):
        db_dir = os.path.join(BASE_DIR, 'data', 'recommenders')
        init_recommender_params = {'neighbourhood_size': 3}
        evaluator = RecommenderEvaluator(
            db_dir, recommender_class=FrequentItemRecommender,
            init_recommender_params=init_recommender_params)
        evaluator.run()
        assert evaluator.f1 > 0
        assert evaluator.precision > 0
        assert evaluator.recall > 0

        init_recommender_params = {'neighbourhood_size': 11}
        evaluator2 = RecommenderEvaluator(
            db_dir, recommender_class=FrequentItemRecommender,
            init_recommender_params=init_recommender_params)
        evaluator2.run()
        assert evaluator2.f1 > 0
        assert evaluator2.precision > 0
        assert evaluator2.recall > 0

    def test_linked_item_recommender(self):
        db_dir = os.path.join(BASE_DIR, 'data', 'recommenders')
        init_recommender_params = {'neighbourhood_size': 2}
        evaluator = RecommenderEvaluator(
            db_dir, recommender_class=LinkedItemRecommender,
            init_recommender_params=init_recommender_params)
        evaluator.run()

        assert evaluator.f1 > 0
        assert evaluator.precision > 0
        assert evaluator.recall > 0

        init_recommender_params = {'neighbourhood_size': 15}
        evaluator2 = RecommenderEvaluator(
            db_dir, recommender_class=LinkedItemRecommender,
            init_recommender_params=init_recommender_params)
        evaluator2.run()

        assert evaluator2.f1 > 0
        assert evaluator2.precision > 0
        assert evaluator2.recall > 0

        assert evaluator2.f1 != evaluator.f1

    def test_mean_predictor_recommender(self):
        db_dir = os.path.join(BASE_DIR, 'data', 'recommenders')

        init_recommender_params = {
            'neighbourhood_size': 2, 'predictor_name': 'mean'
        }

        evaluator = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params)
        evaluator.run()

        assert evaluator.f1 > 0
        assert evaluator.precision > 0
        assert evaluator.recall > 0

        init_recommender_params = {
            'neighbourhood_size': 15, 'predictor_name': 'mean'
        }
        evaluator2 = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params)
        evaluator2.run()

        assert evaluator2.f1 > 0
        assert evaluator2.precision > 0
        assert evaluator2.recall > 0

    def test_collaborative_predictor_recommender(self):
        db_dir = os.path.join(BASE_DIR, 'data', 'recommenders')

        init_recommender_params = {
            'neighbourhood_size': 2, 'predictor_name': 'collaborative'
        }

        evaluator = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params)
        evaluator.run()

        assert evaluator.f1 > 0
        assert evaluator.precision > 0
        assert evaluator.recall > 0

        init_recommender_params = {
            'neighbourhood_size': 15, 'predictor_name': 'collaborative'
        }
        evaluator2 = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params)
        evaluator2.run()

        assert evaluator2.f1 > 0
        assert evaluator2.precision > 0
        assert evaluator2.recall > 0

    def test_resnik_predictor_recommender(self):
        db_dir = os.path.join(BASE_DIR, 'data', 'recommenders')

        init_recommender_params = {
            'neighbourhood_size': 2, 'predictor_name': 'resnik'
        }

        evaluator = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params)
        evaluator.run()

        assert evaluator.f1 > 0
        assert evaluator.precision > 0
        assert evaluator.recall > 0

        init_recommender_params = {
            'neighbourhood_size': 15, 'predictor_name': 'resnik'
        }
        evaluator2 = RecommenderEvaluator(
            db_dir, recommender_class=PredictorRecommender,
            init_recommender_params=init_recommender_params)
        evaluator2.run()

        assert evaluator2.f1 > 0
        assert evaluator2.precision > 0
        assert evaluator2.recall > 0
