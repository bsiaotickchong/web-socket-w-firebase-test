from app import app, socketio

if __name__ == '__main__':
    print("Running app on localhost port 5000...")
    socketio.run(app)
