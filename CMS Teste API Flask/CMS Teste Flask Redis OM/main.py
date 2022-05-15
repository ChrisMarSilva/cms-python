from flask import Flask, request, render_template, make_response
from pydantic import ValidationError
from person import Person
from redis_om.model import NotFoundError
from xml.dom import NotFoundErr
import json
from loguru import logger
from redis_om import Migrator
from dotenv import load_dotenv


app = Flask(import_name=__name__.split('.')[0], template_folder='') 


def build_results(people):
    response = []
    for person in people:
        response.append(person.dict())
    return {"results": response}


@app.route("/person/new", methods=["POST"])
def create_person():
    try:
        # logger.info(f"{request.json=}")
        new_person = Person(**request.json)
        # r = request.json
        # first_name = r['first_name']
        # last_name = r['last_name']
        # age = r['age']
        # address = r['address']
        # skills = r['skills']
        # personal_statement = r['personal_statement']
        # new_person = Person(first_name=first_name, last_name=last_name, age=age, address=address, skills=skills, personal_statement=personal_statement) 
        # logger.info(f"{new_person=}")
        new_person.save()
        return new_person.pk
        # return make_response(json.dumps("123-132"), 200)
    except Exception as e:
        logger.error(e)
        return str(e), 400


@app.route("/person/<id>/age/<int:new_age>", methods=["POST"])
def update_age(id, new_age):
    try:
        person = Person.get(id)
        person.age = new_age
        person.save()
        return "ok" 
    except NotFoundError:
        return "Bad request", 400


@app.route("/person/<id>/delete", methods=["POST"])
def delete_person(id):
    Person.delete(id)
    return "ok"


@app.route("/person/byid/<id>", methods=["GET"])
def find_by_id(id):
    try:
        person = Person.get(id)
        return person.dict()
    except NotFoundError:
        return {}


@app.route("/people/byname/<first_name>/<last_name>", methods=["GET"])
def find_by_name(first_name, last_name):
    people = Person.find((Person.first_name == first_name) & (Person.last_name == last_name)).all()
    return build_results(people)


@app.route("/people/byage/<int:min_age>/<int:max_age>", methods=["GET"])
def find_in_age_range(min_age, max_age):
    people = Person.find((Person.age >= min_age) & (Person.age <= max_age)).sort_by("age").all()
    return build_results(people)


@app.route("/people/byskill/<desired_skill>/<city>", methods=["GET"])
def find_matching_skill(desired_skill, city):
    people = Person.find((Person.skills << desired_skill) & (Person.address.city == city)).all()
    return build_results(people)


@app.route("/people/bystatement/<search_term>", methods=["GET"])
def find_matching_statements(search_term):
    people = Person.find(Person.personal_statement % search_term).all()
    return build_results(people)


@app.route("/person/<id>/expire/<int:seconds>", methods=["POST"])
def expire_by_id(id, seconds):
    try:
        person_to_expire = Person.get(id)
        Person.db().expire(person_to_expire.key(), seconds)
    except NotFoundError:
        pass
    return "ok"


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")    


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, use_reloader=True)  # , debug=True


# py -3 -m venv .venv
# python -m pip install --upgrade aioredis
# python -m pip install --upgrade pydantic
# python -m pip install --upgrade redis
# python -m pip install --upgrade redis-om
# python -m pip uninstall redis-om
# python -m pip install --upgrade redis-om==0.0.20
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py

