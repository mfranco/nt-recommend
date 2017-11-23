from app.models import DB
from app.predictors.mean_predictor import MeanPredictor
from app.predictors.collaborative import (
    CollaborativePredictor, ResnickPredictor)
from app.qa.evaluators import PredictorEvaluator
from flask_philo.test import FlaskTestCase
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
        assert 3.7 == round(
            predictor.predict(user_id='2', item_id='3').rating, 1)

    def test_simple_zero_coverage(self):
        """
        Computing coverage in dataset where all movies have just
        1 rating so is not enough
        """
        dir_name = os.path.join(BASE_DIR, 'data', 'simple')
        evaluator = PredictorEvaluator(dir_name, MeanPredictor)
        evaluator.run()
        assert 0 == evaluator.coverage
        assert evaluator.rmse > 0

    def test_simple_coverage(self):
        """
        Simple coverage metric to calculate the percentage of user
        item pairs for which a rating can be generated
        """
        dir_name = os.path.join(BASE_DIR, 'data', 'simple_coverage')
        evaluator = PredictorEvaluator(dir_name, MeanPredictor)
        prediction_params = {'threshold': 1}
        evaluator.run(predictor_params=prediction_params)
        assert 0.4 == evaluator.coverage
        rmse1 = evaluator.rmse
        coverage1 = evaluator.coverage

        # performance should be worst this time
        evaluator = PredictorEvaluator(dir_name, MeanPredictor)
        prediction_params = {'threshold': 100000}
        evaluator.run(prediction_params=prediction_params)
        assert 0 == evaluator.coverage
        assert rmse1 > evaluator.coverage
        assert coverage1 > evaluator.coverage


class TestCollaborativePredictor(FlaskTestCase):
    def setup(self):
        self.dir_name = os.path.join(BASE_DIR, 'data', 'predictors')
        self.db = DB(db_dir=self.dir_name)
        self.predictor = CollaborativePredictor(
            self.db, neighbourhood_size=100)

    def test_user_msd_similarity(self):
        """
        Computing similarity between users 1 and 2
        """
        # computing similarity bwetween users
        assert 17/4 == round(
            self.predictor.knn.get_user_similarity(
                user_id_1='1', user_id_2='2'), 2)

    def test_similarity_neighbourhoods(self):
        """
        Computing similarity neighbourhoods
        """
        neighbourhood = self.predictor.knn.get_user_neighbourhood(
            user_id='2')
        assert '5' == neighbourhood[0][0]
        assert '4' == neighbourhood[-1][0]

        predictor = CollaborativePredictor(self.db, neighbourhood_size=2)
        neighbourhood = predictor.knn.get_user_neighbourhood(user_id='2')
        assert '5' == neighbourhood[0][0]
        assert '3' == neighbourhood[-1][0]

    def test_prediction(self):
        assert 3.45 == round(
            self.predictor.predict(user_id='2', item_id='3').rating, 2)

    def test_leave_one_collaborative_predictor(self):
        """
        Use mean predictor to test leave one out
        """
        predictor_params = {'neighbourhood_size': 2}
        evaluator = PredictorEvaluator(
            self.dir_name, CollaborativePredictor,
            predictor_params=predictor_params)
        evaluator.run()

    def test_resnick_predictor(self):
        predictor = ResnickPredictor(self.db, neighbourhood_size=2)
        assert 1.074 == round(
            predictor.predict(user_id='2', item_id='3').rating, 3)
