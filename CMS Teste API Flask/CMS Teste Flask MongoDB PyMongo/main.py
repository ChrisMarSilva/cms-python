from flask import Flask, render_template, session, redirect
from functools import wraps
from routes import init_app
from dotenv import load_dotenv


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/


def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap


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
# python -m pip install --upgrade gunicorn
# python -m pip install --upgrade micropython-fcntl
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate


# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5000
# gunicorn -w 1 -b 0.0.0.0:5000 main:app
# gunicorn --workers=1 'test:create_app()'
# gunicorn --bind 0.0.0.0:5000 app:app

