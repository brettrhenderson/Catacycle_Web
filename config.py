import os

class Config(object):
    # used by flask-wtforms for securing web forms
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'