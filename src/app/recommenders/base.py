from app.classifiers import KNN
from app.predictors.collaborative import (
    CollaborativePredictor, ResnickPredictor)
from app.predictors.mean_predictor import MeanPredictor
import operator
import statistics


class BaseRecommender(object):
    """
    Take the union all the items that have been rated by the active user’s
    neighbours.

    Exclude items that have been rated for the active user.

    Rank remaining set by one of the folowing parameters:

    Frequent Item: Number of ratings by item
    Liked Item: Mean of the ratings across neighbours
    Predicted Rating: Make a prediction for each of the candidate items

    The top-N items with the highest scores are returned as
    recommendations
    """

    def __init__(
            self, db, predictor='mean', similarity_metric='msd',
            neighbourhood_size=10, **kwargs):

        predictor_ditc = {
            'collaborative': CollaborativePredictor,
            'resnik': ResnickPredictor,
            'mean': MeanPredictor
        }

        if 'init_predictor_params' in kwargs:
            init_predictor_params = kwargs['init_predictor_params']
        else:
            init_predictor_params = {}

        self.db = db
        self.build_neighbourhood(neighbourhood_size, similarity_metric)
        init_predictor_params['db'] = self.db

        # inject neighbourhood to predictor
        if predictor in ('collaborative', 'resnik'):
            init_predictor_params['knn'] = self.knn
            init_predictor_params['similarity_metric'] = similarity_metric
            init_predictor_params['neighbourhood_size'] = neighbourhood_size

        self.predictor = predictor_ditc[predictor](**init_predictor_params)

        self.user_recommendations = {}

    def build_neighbourhood(self, neighbourhood_size, similarity_metric):
        """
        Uses KNN to build a neighbourhood of users
        """
        self.knn = KNN(
            self.db,
            neighbourhood_size=neighbourhood_size,
            similarity_metric=similarity_metric)

    def rank_recommendations(self, recommendations, user_id):
        """
        Ranks recommendation based in some criteria
        """
        raise NotImplementedError

    def get_user_recommendations(self, user_id, size=10):
        """
        Returns a list of recommendations for a given user.
        """
        # return if recommendation list has been already generated

        if user_id in self.user_recommendations:
            return self.user_recommendations[user_id]

        if user_id not in self.db.users:
            return tuple([])

        user_ratings = self.db.users[user_id].ratings.keys()
        recommendations = set()

        for uid in self.knn.get_user_neighbourhood(user_id=user_id):
            user = self.db.users[uid[0]]

            for movie_id in user.ratings.keys():
                if movie_id not in user_ratings:
                    recommendations.add(movie_id)
        ranked_list = self.rank_recommendations(recommendations, user_id)

        index = 0
        final_recommendations = []

        while index < size:
            if index < len(ranked_list):
                movie_id = ranked_list[index][0]
                index += 1
                final_recommendations.append(self.db.movies[movie_id])
            else:
                break
        self.user_recommendations[user_id] = tuple(final_recommendations)
        return self.user_recommendations[user_id]


class FrequentItemRecommender(BaseRecommender):
    def rank_recommendations(self, recommendations, user_id):
        """
        Ranks a list of items based on the rating frequency by item
        """
        movie_dict = {}
        for movie_id in recommendations:
            movie_dict[movie_id] = len(self.db.movies[movie_id].ratings.keys())
        return sorted(movie_dict.items(), key=operator.itemgetter(1))


class LinkedItemRecommender(BaseRecommender):
    def rank_recommendations(self, recommendations, user_id):
        """
        Ranks a list of items based Mean of the ratings across neighbours
        """
        movie_dict = {}
        for movie_id in recommendations:
            movie_dict[movie_id] = statistics.mean([
                rt.rating for rt in
                self.db.movies[movie_id].ratings.values()])
        return sorted(movie_dict.items(), key=operator.itemgetter(1))


class PredictorRecommender(BaseRecommender):
    def rank_recommendations(self, recommendations, user_id):
        """
        Ranks a list of items based on a prediction for each of the candidate
        items
        """
        movie_dict = {}

        for movie_id in recommendations:
            movie_dict[movie_id] = self.predictor.predict(
                user_id=user_id, item_id=movie_id).rating
        return sorted(movie_dict.items(), key=operator.itemgetter(1))
