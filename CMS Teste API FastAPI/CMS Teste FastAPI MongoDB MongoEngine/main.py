from fastapi import FastAPI
from mongoengine import connect
import router
from dotenv import load_dotenv


app = FastAPI()
# connect(db='test-database-py-fastapi', host='localhost', port=27017, username='root', password='example')
# connect(db='test-database-py-fastapi', host='mongodb://root:example@localhost:27017/', port=27017, username='root', password='example')
connect(host="mongodb://root:example@localhost:27017/test-database-py-fastapi?authSource=admin")
#  connect('test-database-py-fastapi', username='root', password='example', authentication_source='admin')
# connect('workouts', alias='dbworkouts')  # init a connection to database named "workouts" and register it under alias "dbworkouts"
# connect('users', alias='dbusers')  


@app.get("/")
async def home():
    return "Welcome Home"


app.include_router(router.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=5001, reload=True, workers=1)
    # uvicorn.run("src.app:app", host="127.0.0.1", port=8001, log_level="info", reload=True, debug=True)
    # import asyncio
    # from hypercorn.config import Config
    # from hypercorn.asyncio import serve
    # config = Config()
    # config.bind = ["127.0.0.1:5001"]
    # config.use_reloader = True
    # asyncio.run(serve(app, config))


# py -3 -m venv .venv
# python -m pip install --upgrade fastapi
# python -m pip install --upgrade uvicorn
# python -m pip install --upgrade mongoengine
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate

# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5001
