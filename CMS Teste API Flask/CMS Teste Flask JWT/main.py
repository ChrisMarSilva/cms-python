from flask import Flask, request, url_for, redirect
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import bcrypt


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = 'WRB75eA9iHiBSQY2uZsGG8F'  # https://randomkeygen.com/
jwt = JWT(app, authenticate, identity)


@app.route('/')
def login():
    return 'ok'


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter(User.username == username).scalar()
    if bcrypt.check_password_hash(user.password, password):
        return user

@jwt.identity_handler
def identify(payload):
    return User.query.filter(User.id == payload['identity']).scalar()

# @jwt.error_handler
# def error_handler(e):
#     return "Something bad happened", 400

# @jwt.payload_handler
# def make_payload(identity):
#     return {'user_id': identity.id}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-JWT
# python -m pip install --upgrade bcrypt
# python -m pip uninstall pandas -y
# python -m pip uninstall numpy -y
# python -m pip install --upgrade numpy
# python -m pip install --upgrade pandas
# python -m pip install --upgrade Werkzeug
# python -m pip uninstall Werkzeug -y
# python -m pip install Werkzeug==2.0.0
# python main.py
