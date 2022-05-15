from flask import Flask, render_template
from flask_htmlmin import HTMLMIN

app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = 'WRB75eA9iHiBSQY2uZsGG8F'  # https://randomkeygen.com/
app.config['MINIFY_HTML'] = True

htmlmin = HTMLMIN(app)
# htmlmin = HTMLMIN(app, remove_comments=False, remove_empty_space=True, disable_css_min=True)

@app.route('/')
def main():
    # index.html will be minimized !!!
    # index.html será minimizado!!!
    return render_template('index.html')

@app.route('/exempt')
@htmlmin.exempt
def exempted_route():
    # index.html will be exempted and not blessed by holy htmlmin !!!
    # index.html será isento e não abençoado pelo santo htmlmin !!!
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-HTMLmin
# python main.py
