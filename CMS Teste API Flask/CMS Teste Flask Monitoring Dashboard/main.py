from flask import Flask, render_template, redirect, url_for, jsonify
import flask_monitoringdashboard as dashboard



app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/


dashboard.bind(app)


@app.route('/')
def index():
    app.logger.info("Hello there")
    return jsonify({'message': "ok"}), 200


@app.route('/lista')
def lista():
    return jsonify({'message': "ok"}), 200



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade flask_monitoringdashboard

# python main.py

# http://localhost:5000/dashboard
# admin/admin