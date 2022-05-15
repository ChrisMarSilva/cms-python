# import uvicorn
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from src import create_app
from dotenv import load_dotenv


app = create_app()


if __name__ == "__main__":
    # uvicorn.run("main:app", port=5001, reload=True, workers=1)
    # uvicorn.run("src.app:app", host="127.0.0.1", port=8001, log_level="info", reload=True, debug=True)
    config = Config()
    config.bind = ["127.0.0.1:5001"]
    #config.debug = True
    config.use_reloader = True
    asyncio.run(serve(app, config))

# python3 -m venv venv
# source venv/bin/activate

# pip install --upgrade pip
# pip install fastapi[all]
# pip install fastapi
# pip install "uvicorn[standard]"
# pip install "hypercorn[trio]"
# pip install dependency-injector
# pip install sqlalchemy
# pip install requests
# pip install pytest
# pip install pytest-cov
# pip install opentelemetry-launcher
# pip install opentelemetry-instrumentation
# pip install opentelemetry-instrumentation-fastapi
# pip install opentelemetry-instrumentation-sqlalchemy
# pip install opentelemetry-distro
# pip install opentelemetry-api
# pip install opentelemetry-sdk
# pip install opentelemetry-exporter-jaeger
# pip install opentelemetry-exporter-otlp
# pip install opentelemetry-instrumentation-logging
# pip install jinja2
# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]"
# pip install python-multipart
# pip install databases
# pip install aiosqlite
# pip install fastapi_profiler -U
# pip install PyJWT

# uvicorn main:app --reload --port 5001
# hypercorn main:app --worker-class trio

# pip freeze > requirements.txt
# pip install -r requirements.txt