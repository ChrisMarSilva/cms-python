from flask import Flask, render_template, request
from flask_recaptcha import ReCaptcha


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = '4eFvwbWtqafGhCD0Cpwr5GGK4AfHUf2t'  # https://randomkeygen.com/
app.config['RECAPTCHA_ENABLED'] =True
app.config['RECAPTCHA_SITE_KEY'] = "dsfdfsfsd"  #'YOUR_RECAPTCHA_SITE_KEY'
app.config['RECAPTCHA_SECRET_KEY'] = 'vbvcbvcbv' # "aNGYwYjkXx"  #'YOUR_RECAPTCHA_SECRET_KEY'
app.config['RECAPTCHA_THEME'] = "dark" 
app.config['RECAPTCHA_TYPE'] = "image" 
app.config['RECAPTCHA_SIZE'] = "compact" 
app.config['RECAPTCHA_LANGUAGE'] = "en" 
app.config['RECAPTCHA_RTABINDEX'] =10

recaptcha = ReCaptcha(app)
# recaptcha = Recaptcha()
# recaptcha.init_app(app)


@app.route('/')
def index():
    message = ''
    if request.method == 'POST':
        if recaptcha.verify(): message = 'Thanks for filling out the form!'
        else: message = 'Please fill out the ReCaptcha!'
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-reCaptcha
# python main.py
