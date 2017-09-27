class User(object):
    def __init__(self, id):
        self.id = id
        self.ratings = {}
        self.tags = []

    def append_rating(self, rating):
        # index of ratings by movie_id
        self.ratings[rating.movie_id] = rating

    def append_tag(self, tag):
        self.tags.append(tag)
