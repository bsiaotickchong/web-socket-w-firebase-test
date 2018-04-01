from app import app, socketio
from flask import render_template

import os
import requests
import time
import json

FIREBASE_URL = os.environ.get('FIREBASE_URL')


@app.route('/')
def error():
    # notify the user that they need a phone hash (without directly saying)
    return "URL requires identifier"


@app.route('/<phone_hash>')
def index(phone_hash):
    # receive the phone hash and give it to index.html when rendering
    user = {'phone_hash': phone_hash}
    return render_template('index.html', title='Location', user=user)


@app.route('/location/<phone_hash>')
def get_loc_of_hash(phone_hash):
    # get the most recent location update of a phone hash from firebase
    r = requests.get('{}/location/{}.json'.format(FIREBASE_URL, phone_hash))

    if r.json() is None:
        return json.dumps(["No data available"])
    else:
        # @@@@@@@@ not sure why data comes back with a None in the first index... just skip it for now @@@@@@@@@@@
        data = r.json()[1:]
        most_recent_index = len(data) - 1
        location_data = data[most_recent_index]

        return json.dumps(location_data)


@app.route('/close_connection/<phone_hash>')
def close_connection_of_hash(phone_hash):
    # close the connection of the user specified
    pass


@socketio.on('connect event')
def handle_connect(json_data):
    print('connected to {}'.format(json_data['phone_hash']))
    # send to firebase


@socketio.on('location update event')
def handle_loc_update_event(json_data):
    print('Received data from socket...')

    phone_hash = json_data['phone_hash']

    # check if user already has location data in db
    r = requests.get('{}/location/{}.json'.format(FIREBASE_URL, phone_hash))

    # if user has no location data, then start iteration count at 1, otherwise append
    iteration = None
    if r.json() is None:
        iteration = "1"
    else:
        iteration = str(len(r.json()))

    lat = json_data['coords']['latitude']
    lon = json_data['coords']['longitude']
    curr_timestamp = int(time.time())

    payload = {
        iteration: {
            'latitude': str(lat),
            'longitude': str(lon),
            'timestamp': str(curr_timestamp)
            }
        }

    payload = json.dumps(payload, sort_keys=True, indent=4)
    location_url = '{}/location/{}.json'.format(FIREBASE_URL, phone_hash)

    # write to firebase db
    r = requests.patch(location_url, data=payload)
    if r.status_code == 200:
        print('successfully wrote to db')
    else:
        print('failed to write to db, reason: ', r.json())


'''
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass

@socketio.on_error('/chat') # handles the '/chat' namespace
def error_handler_chat(e):
    pass

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    pass
'''
