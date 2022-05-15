from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from config import db
import datetime as dt
import uuid
from bson.objectid import ObjectId
from bson import json_util
import json


class User:


    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return json.dumps(obj=user, default=json_util), 200  # return jsonify(user), 200


    def signup(self):
        print(request.form)
        user = {"_id": uuid.uuid4().hex, "name": request.form.get('name'), "email": request.form.get('email'), "password": request.form.get('password')}
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        if db.users.find_one({"email": user['email']}):
            return json.dumps(obj={"error": "Email address already in use"}), 400  # return jsonify({"error": "Email address already in use"}), 400
        if db.users.insert_one(user):
            db.users_logs.insert_one({"user": user['_id'], "type": 'create', "date": dt.datetime.utcnow()})
            return self.start_session(user)
        return json.dumps(obj={"error": "Signup failed"}), 400  # return jsonify({"error": "Signup failed"}), 400  

    def signout(self):
        user = session['user']
        if user:
            db.users_logs.insert_one({"user": user['_id'], "type": 'logout', "date": dt.datetime.utcnow()})
        session.clear()
        return redirect('/')


    def login(self):
        user = db.users.find_one({"email": request.form.get('email')})
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            db.users_logs.insert_one({"user": user['_id'], "type": 'login', "date": dt.datetime.utcnow()})
            return self.start_session(user)
        return json.dumps(obj={"error": "Invalid login credentials" }), 401  # return jsonify({"error": "Invalid login credentials" }), 401


    def logs(self):
        result = []
        user = session['user']
        if user:
            logs = db.users_logs.find({"user": user['_id']})
            # result = [{"id": str(log["_id"]), "type": log["type"], "date": log["date"]} for log in logs]
            result = list(logs)
            for log in result:
                log["_id"] = str(log["_id"]) 
        return json.dumps(obj={"logs": result}), 200   # return jsonify({"logs": result}), 200


    def select(id: str): 
        result = db.users_logs.find_one({"_id": ObjectId(id)})
        return json.dumps(obj={"message": "user selected", "user": json.dumps(result)}, default=json_util), 200  # return jsonify({"message": "user selected", "user": jsonify(result)}), 200


    def update(id: str): 
        print(request.form)
        result = db.users.update_one({"_id": ObjectId(id)}, {"$set": {"name": request.form['name']}})
        if result.modified_count == 1:
            return json.dumps(obj={"message": "user updated"}, default=json_util), 200  # return jsonify({"message": "user updated"}), 200
        return json.dumps(obj={"error": "user not updated"}, default=json_util), 401  # return jsonify({"error": "user not updated"}), 401


    def delete(id: str):
        result = db.users.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return json.dumps(obj={"message": "user deleted", "id": f"{id}"}, default=json_util), 200  # return jsonify({"message": "user deleted", "id": f"{id}"}), 200
        return json.dumps(obj={"error": "user not updated"}, default=json_util), 401  # return jsonify({"error": "user not updated"}), 401
