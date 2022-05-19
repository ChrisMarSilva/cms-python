from flask import Flask, render_template, request, Blueprint
import flask_limiter
from flask_limiter import Limiter
from flask_limiter import ExemptionScope, Limiter
from flask_limiter.util import get_remote_address


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/




def default_limit_extra():
    if request.headers.get("X-Evil"):
        return "100/minute"
    return "200/minute"

def default_cost():
    if request.headers.get("X-Evil"):
        return 2
    return 1

# limiter = Limiter(
#     app, 
#     key_func=get_remote_address, 
#     default_limits=["2 per minute", "1 per second"],
# )


limiter = Limiter(
    # app,
    key_func=get_remote_address,
    default_limits=["10/second", "1000/hour", default_limit_extra],
    default_limits_exempt_when=lambda: request.headers.get("X-Internal"),
    default_limits_deduct_when=lambda response: response.status_code == 200,
    default_limits_cost=default_cost,
    application_limits=["5000/hour"],
    headers_enabled=True,
)


@app.route('/')
@limiter.limit("5000/day;360/hour;180/minute;5/second")
def index():
    return "ok"


@app.route("/version")
@limiter.exempt
def version():
    return flask_limiter.__version__

@app.route("/slow")
@limiter.limit("1 per day")
def slow():
    return "24"

@app.route("/fast")
def fast():
    return "42"

@app.route("/ping")
@limiter.exempt
def ping():
    return 'PONG'


health_blueprint = Blueprint("health", __name__, url_prefix="/health")

@health_blueprint.route("/")
def health():
    return "ok"

app.register_blueprint(health_blueprint)

limiter.exempt(
    health_blueprint,
    flags=ExemptionScope.DEFAULT | ExemptionScope.APPLICATION | ExemptionScope.ANCESTORS,
)


if __name__ == '__main__':
    limiter.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-Limiter
# python main.py
