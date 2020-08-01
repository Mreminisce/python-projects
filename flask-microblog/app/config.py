import os
from app import app


SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(os.path.dirname(app.root_path), 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTS_PER_PAGE = 25
