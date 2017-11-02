from app.models import DB
from flask_philo.test import FlaskTestCase

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestDensity(FlaskTestCase):
    def setup(self):
        """
        Test computation of matrix density
        """
        fname = os.path.join(BASE_DIR, 'data', 'simple')
        self.db = DB(db_dir=fname)

    def test_densisty(self):
        assert 4/16 == self.db.density
