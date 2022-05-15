from fastapi import FastAPI


app = FastAPI()


@app.get("/", status_code=200)
async def index():
    return {"Hello": "World"}, 200


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5001, log_level="error", reload=False, debug=False, workers=10)
    # uvicorn.run("src.app:app", host="127.0.0.1", port=5001, log_level="info", reload=True, debug=True)
    # import asyncio
    # from hypercorn.config import Config
    # from hypercorn.asyncio import serve
    # config = Config()
    # config.bind = ["127.0.0.1:5001"]
    # config.use_reloader = True
    # asyncio.run(serve(app, config))


# python -m pip install --upgrade fastapi
# python -m pip install --upgrade uvicorn

# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5001
