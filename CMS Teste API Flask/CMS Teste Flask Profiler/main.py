from flask import Flask, jsonify
#import flask_profiler
import time
import asyncio


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = 'dcCLLqRG8eGHCNY8dGW6siWyFguVEaxs'
app.config["DEBUG"] = True
# app.config["flask_profiler"] = {
#     "enabled": app.config["DEBUG"], 
#     "storage": {
#         # "engine": "sqlite",
#         "engine": "mongodb",
#         "MONGO_URL": "mongodb://root:example@localhost:27017",  # ?authSource=admin&maxPoolSize=20&retryWrites=true&w=majority
#         "DATABASE": "flask_profiler",
#         "COLLECTION": "measurements",
#         #  "engine": "sqlalchemy",
#         #  "db_url": "postgresql://user:pass@localhost:5432/flask_profiler"
#         #  "engine": "custom.project.flask_profiler.mysql.MysqlStorage",
#         #  "MYSQL": "mysql://user:password@localhost/flask_profiler",
#     }, 
#     "basicAuth":{"enabled": True, "username": "admin", "password": "admin"}, 
#     "ignore": ["^/static/.*"]
# }


@app.route('/')
async def index():
    return {"Hello": "World"}, 200  # jsonify({'message': "pk"})


# @app.route('/product/<id>', methods=['GET'])
# def getProduct(id):
#     return "product id is " + str(id)


# @app.route('/product/<id>', methods=['PUT'])
# def updateProduct(id):
#     return f"product {id} is being updated"


# @app.route('/products', methods=['GET'])
# async def listProducts(): #  def listProducts(): # async def listProducts(): # 
#     # time.sleep(2)
#     # await asyncio.sleep(1) 
#     return "suppose I send you product list..."


# @app.route('/static/something/', methods=['GET'])
# def staticSomething():
#     return "this should not be tracked..."


# #flask_profiler.init_app(app)


# @app.route('/doSomething', methods=['GET'])
# def doSomething():
#     return "flask-profiler will not measure this."


# @app.route('/doSomethingImportant', methods=['GET'])
# #@flask_profiler.profile()
# def doSomethingImportant():
#     return "flask-profiler will measure this request."


if __name__ == '__main__':
    # app.run(host='localhost', port=5000, debug=True, threaded=True)
    app.run(host='localhost', port=5000, debug=False, threaded=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade flask_profiler
# python -m pip install --upgrade uwsgi
# python -m pip install --upgrade importlib
# python -m pip install --upgrade gunicorn
# python -m pip install --upgrade metaflow

# python main.py

# http://127.0.0.1:5000/flask-profiler/


# uvicorn main:app --reload --port 5000
# gunicorn --workers=10 --threads=2 --timeout=120 --bind=0.0.0.0:5000 main:app
# python  gunicorn -w 4 main:app