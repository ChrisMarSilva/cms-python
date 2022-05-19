from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/
csrf = CSRFProtect(app)


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])

@app.route('/')
def index():
    form = PhotoForm()
    return render_template('index.html', form=form)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-WTF
# python main.py
