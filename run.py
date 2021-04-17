from app import flask_app, socketio

if __name__ == '__main__':
    socketio.run(flask_app, port=5026, host='127.0.0.1', debug=False)