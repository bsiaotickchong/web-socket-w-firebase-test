import os

class Config(object):
	FIREBASE_KEY = os.environ.get('FIREBASE_KEY') or 'key_goes_here'