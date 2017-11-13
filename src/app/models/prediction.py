class Prediction(object):
    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating

    def __str__(self):
        return 'user_id {}, movie_id, rating {} '.format(
            self.user_id, self.movie_id, self.rating
        )

    def __eq__(self, other):
        return (self.user_id == other.user_id) and\
            (self.movie_id == other.movie_id)
