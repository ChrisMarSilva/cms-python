from fastapi import FastAPI, APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random


class ConnectionManager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, message):
        for conn in self.connections:
            print(f'message: {message}')
            await conn.send_text(message)

    def disconnect(self, websocket):
        self.connections.remove(websocket)




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

ws_manager = ConnectionManager()

class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dados")
async def dados():
    return {"message": random.randint(1, 100)}


@app.post('/push')
async def route_b(message: Message, response_model=Message):
    print(f'message: {message.message}')
    await ws_manager.broadcast(message.message)
    return {'message': 'ok'}


@app.websocket('/ws/push')
async def push_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)  # await websocket.accept()x
    while True:
        data = await websocket.receive_text()
        # print(f'data: {data}')
        data = '{"text":"'+str(random.randint(1, 100))+'"}'
        await ws_manager.broadcast(data)  # await websocket.send_text(f"Message text was: {data}")

@app.websocket('/ws/duplex/{user}')
async def push_endpoint(websocket: WebSocket, user: str):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f'data: {data}')
            await ws_manager.broadcast(data)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run("main:app", host="localhost", port=5001, log_level="error", reload=False, debug=False, workers=10)
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
# python -m pip install --upgrade uvicorn[standard]
# python -m pip install --upgrade jinja2


# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5001
