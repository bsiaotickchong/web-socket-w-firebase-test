# web-socket-w-firebase-test
Test application for using a web socket in a Flask application and uploading to Firebase

## How to run
1. Clone and cd into repo
2. Start virtual environment`virtualenv venv`
3. Install relevant dependencies `pip install -r requirements.txt`
4. Initialize environment variables 
`source ./configs.sh` (look at sample.env for env variables you may be missing)
5. `flask run` to run the app (`python3 websocketapp.py` works too)

## Main Requirements:
- Python 3
- Flask 0.12.2
- flask-socketio https://flask-socketio.readthedocs.io/en/latest/
	- eventlet
- Firebase
- Google App Engine

## Resources:
- Deploying to Google cloud:<br>
https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env
- Firebase REST API: <br>
https://firebase.google.com/docs/database/rest/start
