import os

class Config(object):
    # used by flask-wtforms for securing web forms
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    DOWNLOADS = 'temp'