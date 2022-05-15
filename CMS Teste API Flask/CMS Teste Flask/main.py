from flask import Flask, render_template, jsonify
from random import sample
from os import getpid
import json

app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = 'dcCLLqRG8eGHCNY8dGW6siWyFguVEaxs'


@app.route('/')
def index():
    app.logger.info("xxxx")
    pid = str(getpid())
    return render_template('index.html', pid=pid)


@app.route('/calendar')
def calendar():
    app.logger.info("xxxx")
    return render_template('calendar.html')


@app.route('/health', methods=['GET'])
def get(self):
    app.logger.info("xxxx")
    return json.dumps({'success': True, 'message': "healthy"})


@app.route('/data')
def data():
    app.logger.info("xxxx")
    results = sample(range(1, 10), 5)
    return jsonify({'results': results})


# @app.route("/heartbeat")
# def heartbeat():
#    app.logger.info("xxxx")
#     return jsonify({"status": "healthy"})


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)


# python -m pip install --upgrade flask
# python main.py
