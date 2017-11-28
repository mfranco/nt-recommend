from app.models import DB
from app.recommenders import (
    FrequentItemRecommender, LinkedItemRecommender, PredictorRecommender
)
from flask_philo.test import FlaskTestCase

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestRecommenders(FlaskTestCase):
    def setup(self):
        fname = os.path.join(BASE_DIR, 'data', 'predictors')
        self.db = DB(db_dir=fname)

    def test_frequent_item_recommender(self):
