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
        recommender = PredictorRecommender(self.db, predicor='mean')
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)

    def test_collaborative_predictor_recommender(self):
        recommender = PredictorRecommender(self.db, predicor='collaborative')
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)

    def test_resnik_predictor_recommender(self):
        recommender = PredictorRecommender(self.db, predicor='resnik')
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)


class TestEvaluator(FlaskTestCase):

    def test_frequent_item_recommender(self):
        db_dir = os.path.join(BASE_DIR, 'data', 'frequent_item_recommender')
        evaluator = RecommenderEvaluator(
            db_dir, recommender_class=FrequentItemRecommender)
        evaluator.run()
        assert evaluator.f1 > 0
        assert evaluator.precision > 0
        assert evaluator.recall > 0

    def test_linked_item_recommender(self):
        pass

    def test_mean_predictor_recommender(self):
        pass

    def test_collaborative_predictor_recommender(self):
        pass

    def test_resnik_predictor_recommender(self):
        pass
