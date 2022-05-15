from flask import Flask, render_template, jsonify, session, abort, redirect, request, url_for
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import os
import pathlib
import requests


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = 'dcCLLqRG8eGHCNY8dGW6siWyFguVEaxs'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "33204988932-u9hp7j74tvir9ubgpinka6p27sr0l319.apps.googleusercontent.com"

flow = Flow.from_client_secrets_file(
    client_secrets_file=os.path.join(pathlib.Path(__file__).parent, "client_secret.json"),
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper


@app.route('/')
def index():
    app.logger.info("xxxx")
    return "Hello World <a href='/login'><button>Login</button></a> <br/> <a href='/logout'><button>Logout</button></a>"
    # return render_template('index.html')


@app.route("/login")
def login():
    # authorization_url, state = flow.authorization_url()
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    # session['code_verifier'] = flow.code_verifier  # Get and store the code
    session["state"] = state
    return redirect(authorization_url)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/callback")
def callback():
    try:

        flow.fetch_token(authorization_response=request.url)  # code_verifier=False

        if not session["state"] == request.args["state"]:
            abort(500)

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)
        id_info = id_token.verify_oauth2_token(id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID)

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["email"] = id_info.get("email")
        session["picture"] = id_info.get("picture")
        
        return redirect("/protected_area") # protected_area

    except Exception as e:
        app.logger.error(e)
        return redirect("/")


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> Mail {session['email']}! <br/> <img src='{session['picture']}' height='100' width='100'> <a href='/logout'><button>Logout</button></a>"



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)


# https://www.youtube.com/watch?v=FKgJEfrhU1E&list=WL&index=33&t=568s
# https://console.cloud.google.com/apis/credentials?project=flasklogin-350301

# python -m pip install --upgrade flask
# python -m pip install --upgrade google-auth
# python -m pip install --upgrade google-auth-oauthlib
# python main.py

