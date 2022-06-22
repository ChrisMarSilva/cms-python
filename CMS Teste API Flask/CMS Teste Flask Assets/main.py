from flask import Flask, render_template, url_for
from flask_assets import Environment, Bundle
from flask_cors import CORS
import os


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['FLASK_ASSETS_USE_CDN'] = True

CORS(app=app, resources={r'/*': {'origins': '*'}})

assets = Environment(app=app) 
assets.register('css_all', 'style1.css', 'style2.css', output='cached.css', filters='cssmin')
assets.register('js_all', 'main.js', output='cached.js', filters='jsmin')

@app.route('/')
def index():
    app.logger.info("xxxx")
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-Assets
# python -m pip install --upgrade jsmin
# python main.py
