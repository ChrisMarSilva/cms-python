from flask import Flask, session, redirect, Blueprint, jsonify, Response, request
from http import HTTPStatus
from passlib.hash import pbkdf2_sha256
import datetime as dt
import uuid
import json
from models import User, UserLog
from bson.objectid import ObjectId


bp_user = Blueprint('user', __name__, url_prefix='/user')


def start_session(user):
    try:
        del user['password']
    except:
        pass
    user.password = ''
    # try:
    #     user["_id"] = str(user['_id']['$oid'])
    # except:
    #     pass
    # try:
    #     user.pk = str(user['_id']['$oid'])
    # except:
    #     pass
    # print('eeeeeee 02', user.pk)
    # session['user'] = user
    session['logged_in'] = True
    return jsonify(user), 200


@bp_user.route('/signup', methods=['POST'])
def signup():
    try:
        user = User(name=request.form.get('name'), email=request.form.get('email'), password=request.form.get('password'))
        if User.objects(email=user.email).first():
            return jsonify({"error": "Email address already in use"}), 400
        user.password = pbkdf2_sha256.encrypt(user.password)
        user.save()
        UserLog(user=user, type='create', date=dt.datetime.utcnow()).save()
        return start_session(user)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400  


@bp_user.route('/signout', methods=['GET'])
def signout():
    UserLog(user=session['user'], type='logout', date=dt.datetime.utcnow()).save()
    session.clear()
    return redirect('/')


@bp_user.route('/login', methods=['POST'])
def login():
    user = User.objects(email=request.form.get('email')).first()
    if user and pbkdf2_sha256.verify(request.form.get('password'), user.password):
        UserLog(user=user, type='login', date=dt.datetime.utcnow()).save()
        return start_session(user)
    return jsonify({"error": "Invalid login credentials" }), 401


@bp_user.route('/logs', methods=['GET'])
def logs():
    result = []
    user = session['user']
    logs = UserLog.objects(user=ObjectId(user['_id']['$oid']))
    result = [{"type": log.type, "date": log.date} for log in logs]
    # result = json.loads(logs.to_json())
    return jsonify({"logs": result}), 200



# @bp_user.get('/<id>')
# def login_update(id: str):
#     result = db.users_logs.find_one({"_id": ObjectId(id)})
#     return jsonify({"message": "user selected", "user": jsonify(result)}), 200


# @bp_user.put('/<id>')
# def login_update(id: str):
#     print(request.form)
#     result = db.users.update_one({"_id": ObjectId(id)}, {"$set": {"name": request.form['name']}})
#     if result.modified_count == 1:
#         return jsonify({"message": "user updated"}), 200
#     return jsonify({"error": "user not updated"}), 401


# @bp_user.delete('/<id>')
# def login_delete(id: str):
#     result = db.users.delete_one({"_id": id})
#     if result.deleted_count == 1:
#         return jsonify({"message": "user deleted", "id": f"{id}"}), 200
#     return jsonify({"error": "user not updated"}), 401


# employees = Employee.objects().to_json()
# return json.loads(employees)

# employee = Employee.objects().get(pk=id)
# return {"id_": employee.pk, "nome": employee.nome, "age": employee.age, "teams": employee.teams}

# employee = Employee.objects().filter(Q(nome=id) | Q(age=id)).to_json()
# return json.loads(employee)



# @bp_user.route('/cadastro')
# def set_stored_animals():
#     try:
#         _animal = {"name": f"Mike {uuid.uuid4().hex}", "type": "Sem Tipo", "date": dt.datetime.utcnow()}
#         result = db.animal_tb.insert_one(_animal)
#         return Response(response=json.dumps({'message': 'animal created', 'id': f'{result.inserted_id}'}), status=HTTPStatus.CREATED, mimetype="application/json")# return jsonify({"_id": str(result.inserted_id)})
#     except Exception as e:
#         return Response(response=json.dumps({'message': f'{e}'}), status=HTTPStatus.INTERNAL_SERVER_ERROR, mimetype="application/json")


# @bp_user.route('/animals')
# def get_stored_animals():
#     try:
#         _animals = db.animal_tb.find()
#         result = [{"id": str(animal["_id"]), "name": animal["name"], "type": animal["type"]} for animal in _animals]
#         return Response(response=json.dumps({'message': 'ok', 'animals': result}), status=HTTPStatus.OK, mimetype="application/json")  # return jsonify({"animals": result})
#     except Exception as e:
#         return Response(response=json.dumps({'message': f'{e}'}), status=HTTPStatus.INTERNAL_SERVER_ERROR, mimetype="application/json")


def init_app(app):
    app.register_blueprint(bp_user)
