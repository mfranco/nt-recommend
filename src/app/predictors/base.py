from datetime import datetime
from flaskutils import app
from app.qa.util import root_mean_squared_error

import statistics


class BasePredictor(object):
    def __init__(self, db):
        """
        Functionally that is common to all predictors
        """

        self.db = db
        self.predicted_coverage_set = set()

    def get_user_similarity(self, user_id_1, user_id_2):
        """
        Computes similarity between 2 users
        """
        raise NotImplementedError

    def compute_coverage(self):
        """
        Coverage can be computed only for movies that have
        more than threshold_pecertange ratings.
        Every unique combination of item_id, user_id
        where a prediction was possible is stored in order to compute coverage
        Returns the percentage of movies for which a prediction could be made
        """
        return len(self.predicted_coverage_set) / len(self.db.ratings)

    def _inner_loop(self, current_user_id, current_item_id):
        predicted_rating = self.predicted_values[
            (current_user_id, current_item_id,)]

        # if predicted_rating is 0 means that no prediction could be made
        # for the user_id, item_id pair
        if predicted_rating == 0:
            return {}

        # pair of rating and predicted value for all items
        # excluding current_user_id and current_item_id
        predicted_ratings = [
            self.predicted_values[user_item]
            for user_item in self.predicted_values.keys()
            if (user_item[0] != current_user_id and
                user_item[1] != current_item_id)
        ]

        real_rating = 0
        true_ratings = []

        for rating in self.db.ratings:
            if (rating.user_id != current_user_id and
                    rating.movie_id != current_item_id):
                    true_ratings.append(rating.rating)
            else:
                real_rating = rating

        rmse = root_mean_squared_error(true_ratings, predicted_ratings)
        return {
            'rmse': rmse, 'user_id': current_user_id,
            'predicted_rating': predicted_rating,
            'item_id': current_item_id, 'real_rating': real_rating}

    def leave_one_out(self):
        """
        Simple leave-one-out (L1O) testing strategy.

        It uses each (user, item, rating) tuple as a test target.

        Every prediction techniques can be tested by generating
        a predicted  rating  for every  user-item  pair.

        By  comparing every predicted rating to the user-item's actual rating,
        it is possible to compute an error value  for each predictior.

        """
        initial_time = datetime.utcnow()

        self.predictions = []

        app.logger.info('computing all predictions for all ratings')
        self.predicted_values = {}
        for rating in self.db.ratings:
            self.predicted_values[(rating.user_id, rating.movie_id,)] =\
                self.predict(rating.user_id, rating.movie_id)

        app.logger.info('starting Leave One Out')
        index = 0
        for user_item in self.predicted_values.keys():
            if index % 1000 == 0:
                t = ((datetime.utcnow() - initial_time).total_seconds()) / 60
                app.logger.info('{} items in {} minutes\n'.format(index, t))

            r = self._inner_loop(user_item[0], user_item[1])
            if r:
                self.predictions.append(r)

            index += 1

        if self.predictions:
            self.rmse = statistics.mean(
                [pred['rmse'] for pred in self.predictions])
        else:
            self.rmse = 0
        self.coverage = self.compute_coverage()
        self.total_execution_time = (
            (datetime.utcnow() - initial_time).total_seconds()) / 60
        app.logger.info(
            'LILO finished in %s seconds', self.total_execution_time)
