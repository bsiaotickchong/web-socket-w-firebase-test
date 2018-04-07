from app import app, socketio
from flask import render_template

import os
import urllib.request # use instead of "requests", b/c this is supported by Google App Engine
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
    r = urllib.request.Request('{}/location/{}.json'.format(FIREBASE_URL, phone_hash))
    r.add_header('Content-Type','application/json')
    resp = urllib.request.urlopen(r)
    data = resp.read().decode(resp.headers.get_content_charset())       # read and decode with given charset
    data = json.loads(data)                                             # convert to json/list type

    if data is None:
        return json.dumps(["No data available"])
    else:
        # @@@@@@@@ not sure why data comes back with a None in the first index... just skip it for now @@@@@@@@@@@
        data = data[1:]
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
def handle_loc_update_event(loc_data):
    print('Received data from socket...')

    phone_hash = loc_data['phone_hash']
    location_url = '{}/location/{}.json'.format(FIREBASE_URL, phone_hash)

    # check if user already has location data in db
    r = urllib.request.Request(location_url)
    r.add_header('Content-Type','application/json')
    resp = urllib.request.urlopen(r)
    data = resp.read().decode(resp.headers.get_content_charset())       # read and decode with given charset
    data = json.loads(data)                                             # convert to json/list type

    # if user has no location data, then start iteration count at 1, otherwise append
    iteration = None
    if data is None:
        iteration = "1"
    else:
        iteration = str(len(data))

    lat = loc_data['coords']['latitude']
    lon = loc_data['coords']['longitude']
    curr_timestamp = int(time.time())

    payload = {
        iteration: {
            'latitude': str(lat),
            'longitude': str(lon),
            'timestamp': str(curr_timestamp)
            }
        }

    payload = json.dumps(payload, sort_keys=True)

    # write to firebase db
    r = urllib.request.Request(location_url)
    r.get_method = lambda: 'PATCH'                                      # necessary hack to make PATCH requests with urllib.request
    r.add_header('Content-Type','application/json')
    r.add_header('Content-Length',len(payload.encode()))
    resp = urllib.request.urlopen(r, data=payload.encode())
    if resp.getcode() == 200:
        print('successfully wrote to db')
    else:
        data = resp.read().decode(resp.headers.get_content_charset())   # read and decode with given charset
        data = json.loads(data)                                         # convert to json/list type
        print('failed to write to db, reason: ', data)


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
