# import asyncio
import uvicorn
# from hypercorn.config import Config
# from hypercorn.asyncio import serve
from fastapi import FastAPI
from router import router
# from config import config
from dotenv import load_dotenv


app = FastAPI()


@app.get("/")
def home():
    return "Welcome Home"


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5001, reload=True, workers=1)
    # uvicorn.run("src.app:app", host="127.0.0.1", port=8001, log_level="info", reload=True, debug=True)
    # config = Config()
    # config.bind = ["127.0.0.1:5001"]
    # config.use_reloader = True
    # asyncio.run(serve(app, config))

# py -3 -m venv .venv
# python -m pip install --upgrade aioredis
# python -m pip install --upgrade hiredis
# python -m pip install --upgrade httpx
# python -m pip install --upgrade dependency-injector
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate

# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5002