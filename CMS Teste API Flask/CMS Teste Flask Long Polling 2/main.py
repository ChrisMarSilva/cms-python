from loguru import logger
import datetime as dt
import time
from flask import Flask
from flask import render_template
import flask_restful as restful
import os
from dotenv import load_dotenv


app = Flask(import_name=__name__, template_folder='', static_folder='static') # templates
api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class DataUpdate(restful.Resource):

    def _is_updated(self, request_time):
        return os.stat('data.txt').st_mtime > request_time

    def get(self):
        request_time = time.time()
        while not self._is_updated(request_time):
            time.sleep(0.5)
        content = ''
        with open('data.txt') as data:
            content = data.read()
        return {'content': content, 'date': dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}


class Data(restful.Resource):

    def get(self):
        content = ''
        with open('data.txt') as data:
            content = data.read()
        return {'content': content}


api.add_resource(DataUpdate, '/data-update')
api.add_resource(Data, '/data')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


# py -3 -m venv .venv
# python -m pip install --upgrade flask-restful
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
