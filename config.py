import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    UPLOAD_FOLDER = "app\\static\\img"
    PLACEHOLDER_NAME = 'placeholder.jpg'
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(50)
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    DATABASES_FOLDER = os.path.join(basedir,'databases')
    JSON_AS_ASCII = False
    DB_PATH = os.path.join(DATABASES_FOLDER,'db.db')