from .base import BasePredictor
from .similarity import cosine, euclidean, msd, pearson


import operator
import statistics


class CollaborativePredictor(BasePredictor):
    def __init__(
            self, db, threshold=1, similarity_metric='msd',
            neighbourhood_size=100):
        self.threshold = threshold
        sim_dict = {
            'cosine': cosine, 'euclidean': euclidean,
            'msd': msd, 'pearson': pearson}
        self.sim_func = sim_dict[similarity_metric]
        self.neighbourhood_size = neighbourhood_size
        # store neighbourhood by user
        self.neighbourhoods = {}
        self.similarities = {}
        super(CollaborativePredictor, self).__init__(db)

    def normalize(self, user_id_1, user_id_2):
        """
        """
        return 1 - (self.get_user_similarity(
            user_id_1, user_id_2) / self.db.max_diff_ratings)

    def predict(self, user_id,  item_id):
        """
        Based on different  metrics
        """
        neighbourhood = self.get_user_neighbourhood(
            user_id=user_id, size=self.neighbourhood_size)
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
            return 0

        else:
            predicted_rating = sum(above) / sum(below)
            if predicted_rating > 0:
                self.predicted_coverage_set.add((user_id, item_id,))
            return predicted_rating

    def get_user_neighbourhood(self, user_id, size=10):
        """
        Generates user neighbourhood, if neighbourhood have been
        generated previously, it won't be generated again
        """
        if user_id in self.neighbourhoods:
            return self.neighbourhoods[user_id]

        if size > (len(self.db.users.keys()) - 1):
            size = len(self.db.users.keys()) - 1
        similarity_by_user = {}

        for other_user_id in (k for k in self.db.users.keys() if k != user_id):
            similarity_by_user[other_user_id] = self.get_user_similarity(
                user_id_1=user_id, user_id_2=other_user_id)

        sorted_n = sorted(
            similarity_by_user.items(), key=operator.itemgetter(1))
        neighbourhood = [(user[0], user[1]) for user in sorted_n][0: size]
        self.neighbourhoods[user_id] = neighbourhood
        return neighbourhood

    def get_user_similarity(self, user_id_1, user_id_2):
        """
        Compute similarity between two user based in their common
        movies and reviews
        """
        assert user_id_1 in self.db.users
        assert user_id_2 in self.db.users

        # if similarity has been already computed
        if (user_id_1, user_id_2,) in self.similarities:
            return self.similarities[(user_id_1, user_id_2,)]

        user_1_reviews = set(self.db.users[user_id_1].ratings.keys())
        user_2_reviews = set(self.db.users[user_id_2].ratings.keys())

        x, y = [], []
        for movie_id in user_1_reviews.intersection(user_2_reviews):
            x.append(self.db.users[user_id_1].ratings[movie_id].rating)
            y.append(self.db.users[user_id_2].ratings[movie_id].rating)

        if len(x) > 0:
            val = self.sim_func(x, y)

        else:
            val = 0
        self.similarities[(user_id_1, user_id_2,)] = val
        return val


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
        neighbourhood = self.get_user_neighbourhood(
            user_id=user_id, size=self.neighbourhood_size)

        for u in neighbourhood:
            if item_id not in self.db.users[u[0]].ratings:
                # ignoring user with not rating for a given movie
                continue
            # avg rating for user uj
            ruj = self.get_user_rating_avg(u[0])

            # rating for item_id for user uj
            rating_uj = self.db.users[u[0]].ratings[item_id].rating

            # sim between uj and user_id
            sim = self.get_user_similarity(
                user_id_1=user_id, user_id_2=u[0])

            above.append((rating_uj - ruj) * sim)
            below.append(abs(sim))

        if sum(below) == 0:
            return 0

        else:
            predicted_rating = sum(above) / sum(below)
            if predicted_rating > 0:
                self.predicted_coverage_set.add((user_id, item_id,))
            return predicted_rating
