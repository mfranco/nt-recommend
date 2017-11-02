from flask_philo.test import FlaskTestCase
from app.qa.util import mean_squared_error, root_mean_squared_error
import math


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
