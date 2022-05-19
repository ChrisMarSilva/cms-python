import logging
from flask import Flask, render_template, jsonify
from authomatic.extras.flask import FlaskAuthomatic
from authomatic.providers import oauth2, oauth1, openid, gaeopenid


logger = logging.getLogger('authomatic.core')
logger.addHandler(logging.StreamHandler())


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/


fa = FlaskAuthomatic(
    config={
        'tw': {  # Your internal provider name
            # Provider class
            'class_': oauth1.Twitter,
            # Twitter is an AuthorizationProvider so we need to set several other
            # properties too:
            'consumer_key': '########################',
            'consumer_secret': '########################',
        },

        'fb': {
            'class_': oauth2.Facebook,
            # Facebook is an AuthorizationProvider too.
            'consumer_key': '336906656437864',
            'consumer_secret': '2924e6a3a736a99ed5c273532fb55c6b',
            'scope': ['user_about_me', 'email'],
            # 'scope': ['user_about_me', 'email', 'publish_stream', 'read_stream'],
        },
        'gae_oi': {
            # OpenID provider based on Google App Engine Users API.
            # Works only on GAE and returns only the id and email of a user.
            # Moreover, the id is not available in the development environment!
            'class_': gaeopenid.GAEOpenID,
        },
        'oi': {
            # OpenID provider based on the python-openid library.
            # Works everywhere, is flexible, but requires more resources.
            'class_': openid.OpenID,
        },
    },
    secret=app.config['SECRET_KEY'],
    debug=True,
)


@app.route('/')
@fa.login('gae_oi')
def main():
    if fa.result:
        if fa.result.error:
            return fa.result.error.message
        elif fa.result.user:
            if not (fa.result.user.name and fa.result.user.id):
                fa.result.user.update()
            return jsonify(name=fa.result.user.name, id=fa.result.user.id)
    else:
        return fa.response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade authomatic
# python main.py
