from flask import Flask, request, url_for, redirect, jsonify
import tempfile
import flask_sqlalchemy
import flask_praetorian
import flask_cors
import os
import json

db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}


guard = flask_praetorian.Praetorian()
guard.init_app(app, User)

#local_database = tempfile.NamedTemporaryFile(prefix="local", suffix=".db")
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(local_database)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

cors = flask_cors.CORS()
cors.init_app(app)





@app.route('/')
def index():
    return 'ok'


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json(force=True)
    username = req.get("username", None)
    password = req.get("password", None)
    user = guard.authenticate(username, password)
    ret = {"access_token": guard.encode_jwt_token(user).decode('ascii')}  # ascii # utf-8
    return jsonify(ret), 200  # json.dumpsx


@app.route("/protected")
@flask_praetorian.auth_required
def protected():
    return jsonify(message="protected endpoint (allowed user {})".format(flask_praetorian.current_user().username))


@app.route("/protected_admin_required")
@flask_praetorian.roles_required("admin")
def protected_admin_required():
    return jsonify(message="protected_admin_required endpoint (allowed user {})".format(flask_praetorian.current_user().username))


@app.route("/protected_operator_accepted")
@flask_praetorian.roles_accepted("operator", "admin")
def protected_operator_accepted():
    return jsonify(message="protected_operator_accepted endpoint (allowed usr {})".format(flask_praetorian.current_user().username))




if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     db.session.add(User(username="TheDude", hashed_password=guard.hash_password("abides")))
    #     db.session.add(User(username="Walter", hashed_password=guard.hash_password("calmerthanyouare"), roles="admin"))
    #     db.session.add(User(username="Donnie", hashed_password=guard.hash_password("iamthewalrus"), roles="operator"))
    #     db.session.add(User(username="Maude", hashed_password=guard.hash_password("andthorough"), roles="operator,admin"))
    #     db.session.commit()
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade flask-praetorian
# python -m pip uninstall PyJWT -y
# python -m pip install --upgrade PyJWT==1.4.0
# python main.py

# ImportError: cannot import name 'Mapping' from 'collections' (C:\Python310\lib\collections\__init__.py)
# try:
#     from collections.abc import Mapping
# except ImportError:
#     from collections import Mapping