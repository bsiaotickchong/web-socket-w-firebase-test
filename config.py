import os

class Config(object):
    FIREBASE_URL = os.environ.get('FIREBASE_URL') or 'your key'
