from datetime import datetime


class Tag(object):
    def __init__(self, user_id, movie_id, tag, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.tag = tag
        self.timestamp = datetime.utcfromtimestamp(float(timestamp))
