from datetime import datetime


class Rating(object):

    def __init__(self, user_id, movie_id, rating, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = float(rating)
        self.timestamp = datetime.utcfromtimestamp(float(timestamp))

    def __eq__(self, other):
        return (self.user_id == other.user_id) and\
            (self.movie_id == other.movie_id)

    def __str__(self):
        return 'user_id {}, movie_id {}, rating {}, timestamp {}'.format(
                self.user_id, self.movie_id, self.rating, self.timestamp)
