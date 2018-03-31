from app import app, socketio
from flask import render_template

@app.route('/')
def error():
	# notify the user that they need a phone hash (without directly saying)
    return "URL requires identifier" 

@app.route('/<phone_hash>')
def index(phone_hash):
    # receive the phone hash and give it to index.html when rendering
    user = {'phone_hash': phone_hash}
    return render_template('index.html', title='Location', user=user)
	
@app.route('/get_location/<phone_hash>')
def get_loc_of_hash(phone_hash):
    # get the most recent location update of a phone hash from firebase
	pass
	
@app.route('/close_connection/<phone_hash>')
def close_connection_of_hash(phone_hash):
    # close the connection of the user specified
	pass
	
@socketio.on('connect event')
def handle_connect(json):
    print('connected to {}'.format(json['phone_hash']))
    # send to firebase
	
@socketio.on('location update event')
def handle_loc_update_event(json):
    print('updated {} with coords data: '.format(json['phone_hash']) + str(json['coords']))
    # send to firebase
	
	
	
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