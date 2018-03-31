from flask import Flask
from config import Config
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config) # get config/env variables from config.py
socketio = SocketIO(app)

from app import routes # placement avoids circular imports