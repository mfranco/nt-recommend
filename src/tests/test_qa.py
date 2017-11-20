from app.models import DB
from flask_philo.test import FlaskTestCase
from app.qa.util import mean_squared_error, root_mean_squared_error
from app.qa.evaluators import KFold

import math
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestQA(FlaskTestCase):

    def test_mse_exact(self):
        """
        root-mean-squared-error(RMSE)
        """
        y_true = [3, -0.5, 2, 7]
        y_pred = [3, -0.5, 2, 7]
        assert (
            round(0.0, 0) ==
            round(mean_squared_error(y_true, y_pred), 4))

    def test_mse_small(self):
        y_true = [3, -0.5, 2, 7]
        y_pred = [2.5, 0.0, 2, 8]
        assert (
            round(0.375, 4) ==
            round(mean_squared_error(y_true, y_pred), 4))

    def test_mse_big(self):
        y_true = [3, -0.5, 2, 7]
        y_pred = [22.5, 30.0, 32, 68]
        assert (
            round(1482.875, 4) ==
            round(mean_squared_error(y_true, y_pred), 4))

    def test_rmse(self):
        y_true = [3, -0.5, 2, 7]
        y_pred = [2.5, 0.0, 2, 8]
        assert (
            round(math.sqrt(0.375), 4) ==
            round(root_mean_squared_error(y_true, y_pred), 4))


class TestKFold(FlaskTestCase):
    def setup(self):
        self.db_dir = os.path.join(BASE_DIR, 'data', 'predictors')
        self.db = DB(db_dir=self.db_dir)

    def test_leave_one_out(self):
        """
        A leave-one-out takes a dataset of size n and create
        a list of n-folds.
        Every fold is a list of n-1 observations
        Every fold has a list of test data of size 1
        """
        folds = KFold(
            self.db_dir, n_splits=len(self.db.ratings), initialize_db=True)
        # original dataset contains 28 ratings
        assert 28 == folds.total_ratings
        # leave-one-out will generate 28 folds
        assert 28 == len(folds.splits)
        # every split will have (len(self.db.ratings)) - 1 ratings in
        # the train set and 1 in the test set
        for sp in folds.splits:
            assert len(sp['train_set'].ratings) == (folds.total_ratings - 1)
            assert 1 == len(sp['test_set'])

    def test_10_fold(self):
        """
        10 Fold will create 10 folds.
        Each fold will have size of n - math.ceil(n/10) observations.
        Every fold will have a test data list of size math.ceil(n/10)
        """
        folds = KFold(self.db_dir, n_splits=10, initialize_db=True)
        assert 10 == len(folds.splits)
        assert (len(folds.splits[0]['train_set'].ratings)) == (
            len(self.db.ratings) - math.ceil(len(self.db.ratings) / 10))
        assert (len(folds.splits[0]['test_set'])) == (
            math.ceil(len(self.db.ratings) / 10))
