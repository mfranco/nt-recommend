import os

TESTING = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, '../',  'data')

URLS = 'app.urls'

POSTGRESQL_DATABASE_URI = ""

DEBUG = True

BASE_HOSTNAME = 'http://192.168.30.101:8080'

HOST = '0.0.0.0'

USERNAME = 'user'

PASSWORD = 'pass'


LOGGER = {
    'file': True,
    'filename': '~/recommend.log',
    'console': False
}
