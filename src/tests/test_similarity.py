from flask_philo.test import FlaskTestCase
from app.similarity import cosine, euclidean, msd, pearson


class TestSimilarity(FlaskTestCase):
    def test_cosine(self):
        x = [3, 5, 8, 17]
        y = [6, 2, 7, 9]
        assert round(0.9240, 4) == round(cosine(x, y), 4)

    def test_euclidean(self):
        x = [3, 5, 8, 17]
        y = [6, 2, 7, 9]
        assert round(9.110434, 4) == round(euclidean(x, y), 4)

    def test_msd(self):
        x = [3, 4, 3, 2]
        y = [1, 2, 3, 5]
        assert round(17/4, 2) == round(msd(x, y), 2)

    def test_pearson(self):
        x = [1, 2, 1, 1, 2, 3, 1]
        y1 = [2, 1, 2, 2, 1, 2, 2]
        y2 = [2, 4, 2, 2, 4, 6, 2]
        assert -0.372 == round(pearson(x, y1), 3)
        assert 1 == pearson(x, y2)
