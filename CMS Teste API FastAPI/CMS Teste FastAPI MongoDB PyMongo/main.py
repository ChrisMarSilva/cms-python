from fastapi import FastAPI
import router
from dotenv import load_dotenv


app = FastAPI()


@app.get("/")
def home():
    return "Welcome Home"


app.include_router(router.router)


# if __name__ == "__main__":
# import asyncio
# import uvicorn
# from hypercorn.config import Config
# from hypercorn.asyncio import serve
#     uvicorn.run("main:app", port=5001, reload=True, workers=1)
#     uvicorn.run("src.app:app", host="127.0.0.1", port=8001, log_level="info", reload=True, debug=True)
#     config = Config()
#     config.bind = ["127.0.0.1:5001"]
#     config.use_reloader = True
#     asyncio.run(serve(app, config))


# py -3 -m venv .venv
# python -m pip install --upgrade fastapi
# python -m pip install --upgrade uvicorn
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate

# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5001
