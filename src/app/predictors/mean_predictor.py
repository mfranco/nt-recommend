from .base import BasePredictor
from app.models import Prediction

import statistics


class MeanPredictor(BasePredictor):

    def predict(self, user_id,  item_id, threshold=1):
        """
        Simple Baseline predictor.
        Returns the average rating for an item_id, excluding
        the rating given by user_id if exists.
        """
        ratings = [
            item.rating for item
            in self.db.movies[item_id].ratings.values()
            if item.user_id != user_id
        ]

        # if not enough ratings to compute avg, prediciton can not be done
        predicted = 0
        if len(ratings) >= threshold:
            predicted = statistics.mean(ratings)
        return Prediction(user_id, item_id, predicted)
