# import asyncio
# import uvicorn
# from hypercorn.config import Config
# from hypercorn.asyncio import serve
from fastapi import FastAPI, Depends
from dependency_injector.wiring import inject, Provide
from containers import Container
from services import Service
from dotenv import load_dotenv


app = FastAPI()

container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost")
container.config.redis_password.from_env("REDIS_PASSWORD", "")
container.wire(modules=[__name__])


@app.get("/teste")
def home():
    return "Welcome Home"


@app.get("/") # @app.api_route("/")
@inject
async def index(service: Service = Depends(Provide[Container.service])):
    value = await service.process()
    return {"result": value}


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=5001, reload=True, workers=1)
#     uvicorn.run("src.app:app", host="127.0.0.1", port=8001, log_level="info", reload=True, debug=True)
#     config = Config()
#     config.bind = ["127.0.0.1:5001"]
#     config.use_reloader = True
#     asyncio.run(serve(app, config))

# py -3 -m venv .venv
# python -m pip install --upgrade aioredis
# python -m pip install --upgrade hiredis
# python -m pip install --upgrade httpx
# python -m pip install --upgrade dependency-injector
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate

# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5001