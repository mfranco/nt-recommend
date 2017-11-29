from app.models import DB
from app.recommenders import (
    FrequentItemRecommender, LinkedItemRecommender, PredictorRecommender
)
from flask_philo.test import FlaskTestCase

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestRecommenders(FlaskTestCase):
    def setup(self):
        fname = os.path.join(BASE_DIR, 'data', 'recommenders')
        self.db = DB(db_dir=fname)

    def test_frequent_item_recommender(self):
        recommender = FrequentItemRecommender(self.db)
        rec_list = recommender.get_user_recommendations(user_id='1')
        assert 5 == len(rec_list)
