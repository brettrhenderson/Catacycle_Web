import os

class Config(object):
    # used by flask-wtforms for securing web cake_forms
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ab6356e6595fefa0fd3d138539a57f6bcfe95fc2b1e8be79'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024