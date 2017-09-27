from .base import BasePredictor
import statistics


class MeanPredictor(BasePredictor):
    def __init__(self, db, threshold=1):
        self.threshold = threshold
        super(MeanPredictor, self).__init__(db)

    def predict(self, user_id,  item_id):
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

        if len(ratings) < self.threshold:
            # if not enough ratings to compute avg, prediciton can not be done
            return 0
        else:
            predicted = statistics.mean(ratings)
            if predicted > 0:
                self.predicted_coverage_set.add((user_id, item_id,))
            return predicted
