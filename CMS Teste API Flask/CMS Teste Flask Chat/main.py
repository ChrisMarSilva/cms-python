from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from numpy import broadcast


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = 'dcCLLqRG8eGHCNY8dGW6siWyFguVEaxs'
socketio = SocketIO(app=app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    if message != "User connected!":
        send(message, broadcast=True)  # to send the message to all connected clients


# @socketio.on('json')
# def handle_json(json):
#     print('received json: ' + str(json))
#     send(json, json=True)


# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#     emit('my response', args=json)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # socketio.run(app=app, host='localhost', port=5000, debug=True)
    socketio.run(app=app, host='172.26.208.1', port=5000, debug=True)

# python -m pip install --upgrade flask
# python -m pip install --upgrade flask-socketio
# python main.py
