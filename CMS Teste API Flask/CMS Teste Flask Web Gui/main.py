from flask import Flask, render_template
from flaskwebgui import FlaskUI # import FlaskUI
from dotenv import load_dotenv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
ui = FlaskUI(app, width=500, height=500) # add app and parameters


@app.route("/")
def hello():  
    return render_template('index.html')


@app.route("/home", methods=['GET'])
def home(): 
    return render_template('some_page.html')


if __name__ == '__main__':
    ui.run()  # app.run(host='0.0.0.0', port=5000, debug=True)


# py -3 -m venv .venv

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste Internet Speed Test
# .venv\scripts\activate

# python -m pip install --upgrade flaskwebgui

# python flaskwebgui.py
# python gui.py
# python main.py
