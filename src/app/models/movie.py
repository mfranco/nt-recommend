class Movie(object):
    def __init__(self, id, title, genres):
        self.id = id
        self.title = title
        self.genres = genres.split('|')
        self.ratings = {}
        self.tags = []

    def __str__(self):
        return self.id

    def append_rating(self, rating):
        # index of ratings by user_id
        self.ratings[rating.user_id] = rating

    def append_tag(self, tag):
        self.tags.append(tag)
