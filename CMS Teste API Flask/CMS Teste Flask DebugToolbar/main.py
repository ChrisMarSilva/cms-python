from flask import Flask, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import os


app = Flask(import_name=__name__)
app.debug = True
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
# app.config['DEBUG_TB_PANELS'] = ('flask_debugtoolbar.panels.headers.HeaderDebugPanel', 'flask_debugtoolbar.panels.logger.LoggingPanel', 'flask_debugtoolbar.panels.timer.TimerDebugPanel')
# app.config['DEBUG_TB_HOSTS'] = ('127.0.0.1', '::1' )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
# basedir = os.path.join(os.path.dirname(__file__), 'database.db')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')


db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)


class ExampleModel(db.Model):
    __tablename__ = 'examples'
    value = db.Column(db.String(100), primary_key=True)


@app.before_first_request
def setup():
    db.create_all()


@app.route('/')
def index():
    app.logger.info("Hello there")
    ExampleModel.query.get(1)
    ExampleModel.query.get(2)
    ExampleModel.query.get(3)
    ExampleModel.query.get(4)
    ExampleModel.query.get(5)
    return render_template('index.html')


@app.route('/redirect')
def redirect_example():
    response = redirect(url_for('index'))
    response.set_cookie('test_cookie', '1')
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade flask-debugtoolbar

# python main.py
