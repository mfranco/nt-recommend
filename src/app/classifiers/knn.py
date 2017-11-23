from app.similarity import cosine, euclidean, msd, pearson

import operator


class KNN(object):
    """
    Builds a neighbourhood of users based in similarity
    """
    def __init__(self, db, neighbourhood_size=100, similarity_metric='msd'):
        sim_dict = {
            'cosine': cosine, 'euclidean': euclidean,
            'msd': msd, 'pearson': pearson}
        self.sim_func = sim_dict[similarity_metric]
        self.db = db
        self.neighbourhood_size = neighbourhood_size

        # store neighbourhood by user
        self.neighbourhoods = {}
        self.similarities = {}

    def get_user_similarity(self, user_id_1, user_id_2):
        """
        Compute similarity between two user based in their common
        movies and reviews
        """
        if user_id_1 not in self.db.users:
            return 0

        if user_id_2 not in self.db.users:
            return 0

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

    def get_user_neighbourhood(self, user_id):
        """
        Generates user neighbourhood, if neighbourhood have been
        generated previously, it won't be generated again
        """
        if user_id in self.neighbourhoods:
            return self.neighbourhoods[user_id]

        if self.neighbourhood_size > (len(self.db.users.keys()) - 1):
            self.neighbourhood_size = len(self.db.users.keys()) - 1

        similarity_by_user = {}

        for other_user_id in (k for k in self.db.users.keys() if k != user_id):
            similarity_by_user[other_user_id] = self.get_user_similarity(
                user_id_1=user_id, user_id_2=other_user_id)

        sorted_n = sorted(
            similarity_by_user.items(), key=operator.itemgetter(1))
        neighbourhood = [
            (user[0], user[1]) for user in sorted_n][
                0: self.neighbourhood_size]
        self.neighbourhoods[user_id] = neighbourhood
        return neighbourhood
