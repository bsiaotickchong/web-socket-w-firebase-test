# web-socket-w-firebase-test
Test application for using a web socket in a Flask application and uploading to Firebase
1. Use a virtual environment to install flask and dependencies https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    1. cd to the root directory of the repo
    2. Create virtual environment named venv: python3 -m venv venv
    3. Activate the virtual environment: source venv/bin/activate
2. Export the environment variable needed for Flask: export FLASK_APP=websocketapp.py
3. Install dependencies: pip install -r requirements.txt
3. Run the app: flask run

Install all requirements:
1. cd to root of repo
3. pip install -r requirements.txt

Main Requirements:
- Python 3
- Flask 0.12.2
- flask-socketio https://flask-socketio.readthedocs.io/en/latest/
	- eventlet
