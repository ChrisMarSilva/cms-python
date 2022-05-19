from io import BytesIO
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from dotenv import load_dotenv


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
migrate.init_app(app, db)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {file.filename}'
    return render_template('index.html')


@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)

@migrate.configure
def configure_alembic(config):
    # modify config object
    return config

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# py -3 -m venv .venv

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste Internet Speed Test
# .venv\scripts\activate

# python -m pip install --upgrade Flask
# python -m pip install --upgrade Flask-SQLAlchemy
# python -m pip install --upgrade Flask-Migrate
# python main.py
