from flask import Flask
from flask_sslify import SSLify

app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = 'WRB75eA9iHiBSQY2uZsGG8F'  # https://randomkeygen.com/

sslify = SSLify(app)
# sslify = SSLify(app, age=300, subdomains=True, skips=['mypath', 'anotherpath'])


@app.route('/')
def main():
    return 'ok'




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-SSLify
# python main.py
