from .base import BasePredictor
from app.models import Prediction
from app.classifiers import KNN

import statistics


class CollaborativePredictor(BasePredictor):
    def __init__(
            self, db, threshold=1, similarity_metric='msd',
            neighbourhood_size=100):
        self.threshold = threshold
        self.knn = KNN(
            db,
            neighbourhood_size=neighbourhood_size,
            similarity_metric=similarity_metric)
        super(CollaborativePredictor, self).__init__(db)

    def normalize(self, user_id_1, user_id_2):
        """
        """
        return 1 - (self.knn.get_user_similarity(
            user_id_1, user_id_2) / self.db.max_diff_ratings)

    def predict(self, user_id,  item_id):
        """
        Based on different  metrics
        """
        neighbourhood = self.knn.get_user_neighbourhood(
            user_id=user_id)

        above = []
        below = []

        for u in neighbourhood:
            if item_id not in self.db.users[u[0]].ratings:
                # ignoring user with not rating for a given movie
                continue
            weighted_score = self.normalize(user_id, u[0])

            above.append(
                weighted_score * self.db.users[u[0]].ratings[item_id].rating)
            below.append(weighted_score)

        if sum(below) == 0:
            return Prediction(user_id, item_id, 0)

        else:
            predicted = sum(above) / sum(below)
            return Prediction(user_id, item_id, predicted)


class ResnickPredictor(CollaborativePredictor):
    """
    Resnick’s Prediction Formula assumes a correlation based similarity
    function (-1 < sim < 1).

    The target item is assigned a rating that is an adjusted version
    of the target average rating.

    The adjustment is based on the degree to which neighbours rate the target
    item above or below their own average ratings, weighted by the correlation
    between the neighbour and the target user.
    """
    def __init__(
        self, db, threshold=1, similarity_metric='msd',
            neighbourhood_size=100):
        super(ResnickPredictor, self).__init__(
            db, threshold=threshold, similarity_metric=similarity_metric,
            neighbourhood_size=neighbourhood_size)

        self.mean_ratigns_by_user = {}

    def get_user_rating_avg(self, user_id):
        # getting avg rating by user
        if user_id not in self.mean_ratigns_by_user:
            avg_user_rating = statistics.mean([
                r.rating for r in self.db.users[user_id].ratings.values()
            ])
            self.mean_ratigns_by_user[user_id] = avg_user_rating
        else:
            avg_user_rating = self.mean_ratigns_by_user[user_id]
        return avg_user_rating

    def predict(self, user_id,  item_id):
        above = []
        below = []
        neighbourhood = self.knn.get_user_neighbourhood(
            user_id=user_id)

        for u in neighbourhood:
            if item_id not in self.db.users[u[0]].ratings:
                # ignoring user with not rating for a given movie
                continue
            # avg rating for user uj
            ruj = self.get_user_rating_avg(u[0])

            # rating for item_id for user uj
            rating_uj = self.db.users[u[0]].ratings[item_id].rating

            # sim between uj and user_id
            sim = self.knn.get_user_similarity(
                user_id_1=user_id, user_id_2=u[0])

            above.append((rating_uj - ruj) * sim)
            below.append(abs(sim))

        if sum(below) == 0:
            return Prediction(user_id, item_id, 0)

        else:
            predicted = sum(above) / sum(below)
            return Prediction(user_id, item_id, predicted)
