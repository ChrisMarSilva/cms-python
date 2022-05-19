from flask import Flask, render_template, session, redirect
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from functools import wraps
from routes import init_app
from dotenv import load_dotenv


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/
# app.config['MONGODB_DB'] = 'project1'
# app.config['MONGODB_HOST'] = '192.168.1.35'
# app.config['MONGODB_PORT'] = 12345
# app.config['MONGODB_USERNAME'] = 'webapp'
# app.config['MONGODB_PASSWORD'] = 'pwd123'
# app.config['MONGODB_CONNECT'] = False
# app.config['MONGODB_SETTINGS'] = {'db': 'test-database-py-flask', 'host': 'localhost', 'port': 27017, 'username':'root', 'password':'example'}
app.config['MONGODB_SETTINGS'] = {'db': 'test-database-py-flask', 'host': 'mongodb://root:example@localhost:27017/test-database-py-flask?authSource=admin'}
# app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']

db = MongoEngine()
db.init_app(app)
# app.session_interface = MongoEngineSessionInterface(db)

# toolbar = DebugToolbarExtension(app) 
# toolbar.init_app(app)


def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap

@app.route('/startup')
def startup():
    print('  == > startup')
    return 'Server startup...'

@app.route('/shutdown')
def shutdown():
    print('  == > shutdown')
    return 'Server shutting down...'


@app.route('/')
def home():
  return render_template('home.html')


@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')
  

init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


# py -3 -m venv .venv
# python -m pip install --upgrade wheel
# python -m pip install --upgrade dnspython
# python -m pip install --upgrade mongoengine
# python -m pip install --upgrade flask-mongoengine
# python -m pip install --upgrade flask-debugtoolbar
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate


# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5000
# gunicorn -w 1 -b 0.0.0.0:5000 main:app
# gunicorn --workers=1 'test:create_app()'
# gunicorn --bind 0.0.0.0:5000 app:app

