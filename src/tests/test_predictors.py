from app.models import DB
from flask_philo.test import FlaskTestCase
from app.predictors.mean_predictor import MeanPredictor
from app.predictors.collaborative import (
    CollaborativePredictor, ResnickPredictor)
from app.predictors.similarity import cosine, euclidean, msd, pearson

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestSimpleMeanPredictor(FlaskTestCase):
    def setup(self):
        fname = os.path.join(BASE_DIR, 'data', 'predictors')
        self.db = DB(db_dir=fname)

    def test_mean_predictor(self):
        """
        Predicting rating for user 1 movie 1
        """
        predictor = MeanPredictor(self.db)
        assert 3.7 == round(predictor.predict(user_id='2', item_id='3'), 1)

    def test_simple_zero_coverage(self):
        """
        Computing coverage in dataset where all movies have just
        1 rating so is not enough
        """
        fname = os.path.join(BASE_DIR, 'data', 'simple')
        db = DB(db_dir=fname)
        predictor = MeanPredictor(db)
        predictor.leave_one_out()
        assert 0 == predictor.coverage

    def test_simple_coverage(self):
        """
        Simple coverage metric to calculate the percentage of user
        item pairs for which a rating can be generated
        """
        fname = os.path.join(BASE_DIR, 'data', 'simple_coverage')
        db = DB(db_dir=fname)
        predictor = MeanPredictor(db, threshold=1)
        predictor.leave_one_out()
        assert 0.4 == predictor.coverage
        predictor = MeanPredictor(db, threshold=10000)
        predictor.leave_one_out()
        assert 0 == predictor.coverage


class TestDistance(FlaskTestCase):
    def test_cosine(self):
        x = [3, 5, 8, 17]
        y = [6, 2, 7, 9]
        assert round(0.9240, 4) == round(cosine(x, y), 4)

    def test_euclidean(self):
        x = [3, 5, 8, 17]
        y = [6, 2, 7, 9]
        assert round(9.110434, 4) == round(euclidean(x, y), 4)

    def test_msd(self):
        x = [3, 4, 3, 2]
        y = [1, 2, 3, 5]
        assert round(17/4, 2) == round(msd(x, y), 2)

    def test_pearson(self):
        x = [1, 2, 1, 1, 2, 3, 1]
        y1 = [2, 1, 2, 2, 1, 2, 2]
        y2 = [2, 4, 2, 2, 4, 6, 2]
        assert -0.372 == round(pearson(x, y1), 3)
        assert 1 == pearson(x, y2)


class TestCollaborativePredictor(FlaskTestCase):
    def setup(self):
        fname = os.path.join(BASE_DIR, 'data', 'predictors')
        self.db = DB(db_dir=fname)
        self.predictor = CollaborativePredictor(
            self.db, neighbourhood_size=100)

    def test_user_msd_similarity(self):
        """
        Computing similarity between users 1 and 2
        """
        # computing similarity bwetween users
        assert 17/4 == round(
            self.predictor.get_user_similarity(
                user_id_1='1', user_id_2='2'), 2)

    def test_similarity_neighbourhoods(self):
        """
        Computing similarity neighbourhoods
        """
        neighbourhood = self.predictor.get_user_neighbourhood(
            user_id='2', size=4)
        assert '5' == neighbourhood[0][0]
        assert '4' == neighbourhood[-1][0]

        predictor = CollaborativePredictor(self.db, neighbourhood_size=100)
        neighbourhood = predictor.get_user_neighbourhood(user_id='2', size=2)
        assert '5' == neighbourhood[0][0]
        assert '3' == neighbourhood[-1][0]

    def test_prediction(self):
        assert 3.45 == round(
            self.predictor.predict(user_id='2', item_id='3'), 2)

    def test_leave_one_collaborative_predictor(self):
        """
        Use mean predictor to test leave one out
        """
        predictor = CollaborativePredictor(self.db, neighbourhood_size=2)
        predictor.leave_one_out()

    def test_resnick_predictor(self):
        predictor = ResnickPredictor(self.db, neighbourhood_size=2)
        assert 1.074 == round(predictor.predict(user_id='2', item_id='3'), 3)
