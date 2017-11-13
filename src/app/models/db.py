from flask_philo import app
from app.models import Rating, Movie, User, Tag
from app.nlp.utils import tokenize

import csv
import os
import statistics


class DB(object):
    def __init__(self, db_dir=None, ratings_to_exlude=None):
        """
        Encapsulates all information related to reatings, movies and user
        in one single class easy to access
        """
        if db_dir is None:
            self.db_dir = os.path.join(
                app.config['DATA_DIR'], 'db', 'ml-latest-small')
        else:
            self.db_dir = db_dir

        if ratings_to_exlude is None:
            self.ratings_to_exlude = []
        else:
            self.ratings_to_exlude = ratings_to_exlude

        self.load_tags()
        self.load_ratings()
        self.load_movies()
        self.load_users()

        self.compute_density()
        self.compute_stats()

        unique_ratings = set()
        for record in self.ratings:
            unique_ratings.add(record.rating)
        self.max_diff_ratings = (
            min(unique_ratings) - max(unique_ratings)) ** 2

    def load_tags(self):
        """
        Loads in memory tags database
        """
        fname = os.path.join(self.db_dir, 'tags.csv')
        with open(fname) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)
            self.tags = tuple(Tag(*row) for row in reader)

    def load_ratings(self):
        """
        Loads in memory ratings database.
        It ignores ratings described in ratings_to_exlude
        """
        fname = os.path.join(self.db_dir, 'ratings.csv')
        rt_list = []
        with open(fname) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)
            for row in reader:
                rt = Rating(*row)
                if (rt.user_id, rt.movie_id,) not in self.ratings_to_exlude:
                    rt_list.append(rt)
        self.ratings = tuple(rt_list)

    def load_movies(self):
        """
        Loads in memory movies database
        """
        fname = os.path.join(self.db_dir, 'movies.csv')
        self.movies = {}
        with open(fname) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)
            for row in reader:
                movie = Movie(*row)
                self.movies[movie.id] = movie

        for rating in self.ratings:
            if rating.movie_id in self.movies:
                self.movies[rating.movie_id].append_rating(rating)

        for tag in self.tags:
            self.movies[tag.movie_id].append_tag(tag)

    def load_users(self):
        """
        Loads in memory users and ratings by every user
        """
        self.users = {}

        for rating in self.ratings:
            if rating.user_id in self.users:
                self.users[rating.user_id].append_rating(rating)
            else:
                user = User(rating.user_id)
                user.append_rating(rating)
                self.users[rating.user_id] = user

        for tag in self.tags:
            self.users[tag.user_id].append_tag(tag)

    def compute_density(self):
        """
        Density is the number of ratings / total posible ratings
        """
        self.total_users = len(self.users.keys())
        self.total_movies = len(self.movies.keys())

        # users is a dictionary where every key is a user and movies another
        # dict where very key represents a movie
        self.total_posible_ratings = self.total_users * self.total_movies

        # movies is a dictionary with movie_id as key and total ratings
        # for that movie as value, so the sum of all values is the number
        # of total ratings for all movies
        total_ratings = sum(
            [len(movie.ratings.keys()) for movie in self.movies.values()])

        self.density = total_ratings / self.total_posible_ratings

    def compute_stats(self):
        """
        Mean, median, standard deviation, max, min ratings per user
        and movie
        """

        self.stats = {}

        users = {}
        # number of ratings by user
        user_ratings_count = [
            len(user.ratings.keys()) for user in self.users.values()]
        users['mean'] = statistics.mean(user_ratings_count)
        users['median'] = statistics.median(user_ratings_count)
        users['sd'] = statistics.stdev(user_ratings_count)
        users['min'] = min(user_ratings_count)
        users['max'] = max(user_ratings_count)

        self.stats['users'] = users

        movies = {}
        # number of ratings by movie
        movie_ratings_count = [
            len(movie.ratings.keys()) for movie in self.movies.values()]
        movies['mean'] = statistics.mean(movie_ratings_count)
        movies['median'] = statistics.median(movie_ratings_count)
        movies['sd'] = statistics.stdev(movie_ratings_count)
        movies['min'] = min(movie_ratings_count)
        movies['max'] = max(movie_ratings_count)

        self.stats['movies'] = movies

        total_ratings = {}

        for r in self.ratings:
            if r.rating in total_ratings:
                total_ratings[r.rating] += 1
            else:
                total_ratings[r.rating] = 1
        self.stats['ratings'] = total_ratings

        tags = {}
        # normalized tags
        n_tags = []
        for t in self.tags:
            n_tags.extend(tokenize(t.tag))
        self.normalized_tags = set(n_tags)

        # number of tags by user
        by_user = {}
        by_user['count'] = [len(u.tags) for u in self.users.values()]
        by_user['mean'] = statistics.mean(by_user['count'])
        by_user['median'] = statistics.median(by_user['count'])
        by_user['sd'] = statistics.stdev(by_user['count'])
        by_user['min'] = min(by_user['count'])
        by_user['max'] = max(by_user['count'])
        tags['by_user'] = by_user

        # number of tags by movie
        by_movie = {}
        by_movie['count'] = [len(m.tags) for m in self.movies.values()]
        by_movie['mean'] = statistics.mean(by_movie['count'])
        by_movie['median'] = statistics.median(by_movie['count'])
        by_movie['sd'] = statistics.stdev(by_movie['count'])
        by_movie['min'] = min(by_movie['count'])
        by_movie['max'] = max(by_movie['count'])
        tags['by_movie'] = by_movie
        self.stats['tags'] = tags
