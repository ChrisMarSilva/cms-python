from flask import Flask, render_template, jsonify
from random import sample
from flask_pymongo import PyMongo


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/
app.config["MONGO_DBNAME"] = "test-database-py-flask"
app.config["MONGO_URI"] = 'mongodb://root:example@localhost:27017/test-database-py-flask?authSource=admin&maxPoolSize=20&retryWrites=true&w=majority'

mongo = PyMongo(app)



@app.route('/')
def index():
    data = [("01-01-2020", 1597), ("02-01-2020", 1456), ("03-01-2020", 1908), ("04-01-2020", 896), ("05-01-2020", 755), ("06-01-2020", 453), ("07-01-2020", 1100), ("08-01-2020", 1235), ("09-01-2020", 1478)]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('index.html', labels=labels, values=values)


@app.route('/data')
def data():
    try:
        charts = mongo.db.charts
        results = charts.find_one({'name': 'Chart1'})
        results = results['values']
    except:
        results = sample(range(1, 10), 5)
    return jsonify({'results': results})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-PyMongo
# python main.py
