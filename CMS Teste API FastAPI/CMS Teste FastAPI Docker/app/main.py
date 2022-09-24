import logging
from http import HTTPStatus
from typing import Dict
from fastapi import FastAPI
from .routers import order


logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__file__)


app = FastAPI(title='Your Fruit Self Service',version='1.0.0', description='Order your fruits here', root_path='')
app.include_router(order.router)


@app.get("/", status_code=HTTPStatus.OK)
async def root() -> Dict[str, str]:
    """
    Endpoint for basic connectivity test.
    """
    logger.info('root called')
    return {'message': 'I am alive'}
    # return {"Hello": "World"}, 200


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="localhost", port=5001, log_level="error", reload=False, debug=False, workers=10)
    # uvicorn.run("src.app:app", host="127.0.0.1", port=5001, log_level="info", reload=True, debug=True)
    # import asyncio
    # from hypercorn.config import Config
    # from hypercorn.asyncio import serve
    # config = Config()
    # config.bind = ["127.0.0.1:5001"]
    # config.use_reloader = True
    # asyncio.run(serve(app, config))


# python -m pip install --upgrade pip
# python -m pip install --upgrade fastapi
# python -m pip install --upgrade uvicorn
# python -m pip install --upgrade requests
# python -m pip install --upgrade beautifulsoup4

# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5001
