from flask import Flask, render_template, jsonify, session, abort, redirect, request, url_for
from authlib.integrations.flask_client import OAuth, OAuthError
import os


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')
app.config['TWITTER_CLIENT_ID'] = os.getenv('TWITTER_CLIENT_ID')
app.config['TWITTER_CLIENT_SECRET'] = os.getenv('TWITTER_CLIENT_SECRET')


oauth = OAuth(app=app)

# google = oauth.register(
#     name = 'google',
#     client_id = app.config["GOOGLE_CLIENT_ID"],
#     client_secret = app.config["GOOGLE_CLIENT_SECRET"],
#     access_token_url = 'https://oauth2.googleapis.com/token',  # 'https://accounts.google.com/o/oauth2/token',
#     access_token_params = None,
#     authorize_url = 'https://accounts.google.com/o/oauth2/auth',
#     authorize_params = None,
#     api_base_url = 'https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
#     client_kwargs = {'scope': 'openid email profile'},
# )

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
)


github = oauth.register(
    name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)


@app.route('/')
def index():
    app.logger.info("index")
    user = session.get('user')
    return render_template('index.html', user=user)



@app.errorhandler(OAuthError)
def handle_error(error):
    return render_template('error.html', error=error)


@app.route('/login/google')
def google_login():
    app.logger.info("login/google")
    # google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    # return google.authorize_redirect(redirect_uri)
    # redirect_uri = url_for('callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


#@app.route("/callback")
#def callback():
@app.route('/login/google/authorize')
def google_authorize():
    # google = oauth.create_client('google')
    # token = google.authorize_access_token()
    # resp = google.get('userinfo').json()
    # return "You are successfully signed in using google"
    token = oauth.google.authorize_access_token()
    resp = token.get('userinfo')
    if resp: session['user'] = resp
    app.logger.info(f"{resp=}")
    return redirect('/')


@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    if resp: session['user'] = resp
    app.logger.info(f"{resp=}")
    return "You are successfully signed in using github"








@app.route('/login/twitter')
def twitter_login():
    try:
        redirect_uri = url_for('twitter_authorize', _external=True)
        return oauth.twitter.authorize_redirect(redirect_uri)
    except Exception as e:
        app.logger.error(e)
        return redirect("/")


@app.route('/login/twitter/authorize')
def twitter_authorize():
    try:
        # token = oauth.twitter.authorize_access_token()
        # app.logger.info(f'{token=}')
        # resp = oauth.twitter.get('account/verify_credentials.json', params={'skip_status': True})
        # app.logger.info(f'{resp.json()=}')
        # # DON'T DO IT IN PRODUCTION, SAVE INTO DB IN PRODUCTION
        # session['token'] = token
        # session['user'] = resp.json()
        return redirect('/')
    except Exception as e:
        app.logger.error(e)
        return redirect("/")



@app.route('/tweets')
def list_tweets():
    url = 'statuses/user_timeline.json'
    params = {'include_rts': 1, 'count': 200}
    prev_id = request.args.get('prev')
    if prev_id: params['max_id'] = prev_id
    resp = oauth.twitter.get(url, params=params)
    tweets = resp.json()
    return render_template('tweets.html', tweets=tweets)



@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('token', None)
    return redirect('/')


# if __name__ == '__main__':
#     # app.run(host='localhost', port=5000, debug=True, threaded=True)
#     app.run(port=5000, debug=True, threaded=True)


# https://console.cloud.google.com/apis/credentials?project=flasklogin-350301

# python -m pip install --upgrade flask
# python -m pip install --upgrade Authlib
# python main.py

# pip install -U Flask Authlib requests
# export FLASK_APP=main.py
# flask run

# http://flask.com.br
# C:\Windows\System32\Drivers\etc\hosts