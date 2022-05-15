from loguru import logger
import datetime as dt
import time
from random import randint
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv


app = Flask(import_name=__name__, template_folder='', static_folder='static') # templates


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/poll")
def poll():
    print('====> poll')
    time.sleep(10.0)
    # Fetch from https://randomwordgenerator.com/phrase.php
    arr = ["Let Her Rip", "A Dime a Dozen", "Quick and Dirty", "Two Down, One to Go", "Head Over Heels", "Under the Weather", "Long In The Tooth", "Hit Below The Belt", "Cry Over Spilt Milk", "Put a Sock In It", "Poke Fun At", "Down For The Count", "Goody Two-Shoes", "Drive Me Nuts"]    
    choice = randint(0, len(arr) - 1)
    return jsonify({"user": "johndoe", "message": arr[choice], "category": "phrases", "timestamp": dt.datetime.now()})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


# py -3 -m venv .venv
# python -m pip install --upgrade xxxxxxx
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
