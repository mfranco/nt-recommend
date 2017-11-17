from app.models import DB
from flask_philo import app
from datetime import datetime
from app.qa.util import root_mean_squared_error

import math
import statistics


class PredictionResult(object):
    def __init__(self, prediction, real_rating):
        self.prediction = prediction
        self.real_rating = real_rating


class BaseEvaluator(object):
    """
    Common functionally for performance evaluation
    """

    def compute_coverage(self):
        """
        Computes the percentage of users where a prediction or
        recommendation was possible
        """
        _sum = 0
        if len(self.recommendations.keys()) == 0:
            return 0

        for user_id, user_recommendations in self.recommendations.items():
            user = self.db.users[user_id]

            if len(user.ratings.keys()) == 0:
                continue
            _sum += len(user_recommendations) / len(user.ratings)
        self.coverage = _sum / len(self.recommendations.keys())

    def compute_precision(self, top_n):
        """
        Computes the mean precision (over all test users) for a given
        recommendation list size
        """
        _sum = 0
        if len(self.recommendations.keys()) == 0:
            return 0

        if top_n > 0:
            return 0

        for user_id, user_recommendations in self.recommendations.items():
            intersection = self._get_intersection(
                user_id, user_recommendations, top_n)
            size = len(intersection)
            _sum += (size / top_n)
        self.precision = _sum / len(self.recommendations.keys())

    def compute_recall(self, top_n):
        """
        Computes the mean recall (over all test users) for a given
        recommendation list size
        """
        _sum = 0
        if len(self.recommendations.keys()) == 0:
            return 0

        if top_n > 0:
            return 0

        for user_id, user_recommendations in self.recommendations.items():
            user = self.db.users[user_id]

            if len(user.ratings.keys()) == 0:
                continue

            intersection = self._get_intersection(
                user_id, user_recommendations, top_n)
            _sum += len(intersection) / len(user.ratings.keys())

        self.recall = _sum / len(self.recommendations.keys())

    def compute_f1(self):
        """
        Computes F1 Measure
        """
        if not hasattr('recall', self):
            self.compute_recall()
            self.compute_precision()

        self.f1 = (2 * self.recall * self.precision) /\
            (self.recall + self.precision)

    def _get_intersection(self, user_id, user_recommendations, top_n):
        """
        Computes the intersection between the items that has been recommended
        to a user and the real items that the user has rated
        """
        user = self.db.users[user_id]
        intersection = []
        counter = 0

        for item_id in user_recommendations:
            if counter < len(user_recommendations):
                counter += 1

                if item_id in user.ratings:
                    intersection.append(item_id)
            else:
                break

        return intersection


class KFold(object):
    def __init__(self, db_dir, n_splits=None, **kwargs):
        """
        Divides all samples in k groups of samples.
        If n_splits is None, it will generate
        Total Number of Ratings folds (Leave-One-Out) Style
        """
        self.db_dir = db_dir
        self.db = DB(db_dir=self.db_dir)
        if n_splits is None:
            n_splits = len(self.db.ratings)
        self._split(n_splits)

    def _split(self, n_splits):
        app.logger.info('Creating K-fold {} splits'.format(n_splits))
        index = 0
        split_db_list = []
        jump_size = math.ceil(len(self.db.ratings) / n_splits)

        while index < len(self.db.ratings):
            idx = 0
            rt_to_exclude = []
            test_set = []
            while idx < len(self.db.ratings):
                if idx == index:
                    jump_index = 0
                    while jump_index < jump_size:
                        if idx == len(self.db.ratings):
                            break

                        rt = self.db.ratings[idx]
                        rt_to_exclude.append((rt.user_id, rt.movie_id,))
                        test_set.append(rt)
                        idx += 1
                        jump_index += 1
                    db = DB(
                        db_dir=self.db_dir, ratings_to_exlude=rt_to_exclude)
                    split_db_list.append(
                        {'train_set': db, 'test_set': test_set})
                else:
                    idx += 1
            index += jump_size

        # make test set and split immutable objects
        self.splits = tuple(split_db_list)


class PredictorEvaluator(object):
    def __init__(self, db_dir, predictor_class, **kwargs):
        """
        Evaluates Prediction performance
        """
        self.initial_time = datetime.utcnow()
        n_splits = kwargs.get('n_splits')
        if 'predictor_params' in kwargs:
            predictor_params = kwargs['predictor_params']
        else:
            predictor_params = {}

        self.folds = KFold(db_dir, n_splits=n_splits)
        self.n_splits = len(self.folds.splits)
        self.predictors = tuple([
            {
                'test_set': split['test_set'],
                'predictor': predictor_class(
                    split['train_set'], **predictor_params)
            }
            for split in self.folds.splits
        ])

    def compute_metrics(self):
        """
        Coverage: Percentange of ratings where a prediction was possible
        RMSE: Root Mean Square Error
        """
        coverage_list = []
        rmse_list = []
        for result in self.evaluator_predictions:
            true_ratings = []
            predicted_ratings = []
            iteration_predictions = []

            for record in result['predictions']:
                if record.prediction.rating > 0:
                    iteration_predictions.append(1)
                else:
                    iteration_predictions.append(0)

                predicted_ratings.append(record.prediction.rating)
                true_ratings.append(record.real_rating)
            coverage_list.append(
                sum(iteration_predictions) / result['test_set_size'])
            rmse_list.append(
                root_mean_squared_error(true_ratings, predicted_ratings))
        self.coverage = statistics.mean(coverage_list)
        self.rmse = statistics.mean(rmse_list)

    def run(self, *args, **kwargs):
        """
        Runs Predictors expiriments KFold Validation

        """


        app.logger.info('Running KFold Validation ')
        self.evaluator_predictions = []

        if 'predictor_params' in kwargs:
            predictor_params = kwargs['predictor_params']
        else:
            predictor_params = {}

        for predictor in self.predictors:
            prd = predictor['predictor']
            iteration_predictions = []
            for test_pred in predictor['test_set']:
                real_rating = test_pred.rating

                prediction = prd.predict(
                    user_id=test_pred.user_id, item_id=test_pred.movie_id,
                    **predictor_params
                )

                iteration_predictions.append(
                    PredictionResult(prediction, real_rating)
                )
            self.evaluator_predictions.append({
                'predictions': iteration_predictions,
                'test_set_size': len(predictor['test_set'])
            })

        self.compute_metrics()

        self.total_execution_time = (
            (datetime.utcnow() - self.initial_time).total_seconds()) / 60
        app.logger.info(
            'Execution finished in %s minutes', self.total_execution_time)
