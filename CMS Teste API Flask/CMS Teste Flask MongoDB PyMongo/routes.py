from flask import Blueprint, jsonify, Response, request
from http import HTTPStatus
import datetime as dt
import uuid
import json
from config import db
from models import User


bp_user = Blueprint('user', __name__, url_prefix='/user')


@bp_user.route('/signup', methods=['POST'])
def signup():
    return User().signup()


@bp_user.route('/signout', methods=['GET'])
def signout():
    return User().signout()


@bp_user.route('/login', methods=['POST'])
def login():
    return User().login()


@bp_user.put('/<id>')
def login_update(id: str):
    return User().update(id=id)


@bp_user.delete('/<id>')
def login_delete(id: str):
    return User().delete(id=id)


@bp_user.route('/logs', methods=['GET'])
def logs():
    return User().logs()


@bp_user.route('/cadastro')
def set_stored_animals():
    try:
        _animal = {"name": f"Mike {uuid.uuid4().hex}", "type": "Sem Tipo", "date": dt.datetime.utcnow()}
        result = db.animal_tb.insert_one(_animal)
        return Response(response=json.dumps({'message': 'animal created', 'id': f'{result.inserted_id}'}), status=HTTPStatus.CREATED, mimetype="application/json")# return jsonify({"_id": str(result.inserted_id)})
    except Exception as e:
        return Response(response=json.dumps({'message': f'{e}'}), status=HTTPStatus.INTERNAL_SERVER_ERROR, mimetype="application/json")


@bp_user.route('/animals')
def get_stored_animals():
    try:
        _animals = db.animal_tb.find()
        result = [{"id": str(animal["_id"]), "name": animal["name"], "type": animal["type"]} for animal in _animals]
        return Response(response=json.dumps({'message': 'ok', 'animals': result}), status=HTTPStatus.OK, mimetype="application/json")  # return jsonify({"animals": result})
    except Exception as e:
        return Response(response=json.dumps({'message': f'{e}'}), status=HTTPStatus.INTERNAL_SERVER_ERROR, mimetype="application/json")


def init_app(app):
    app.register_blueprint(bp_user)
