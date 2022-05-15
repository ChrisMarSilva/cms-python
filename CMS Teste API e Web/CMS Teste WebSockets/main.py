#!/usr/bin/env python
import asyncio
import websockets
from dotenv import load_dotenv


# async def handler(websocket, path):
#     message = await websocket.recv()
#     reply = f"Data recieved as:  {message}!"
#     await websocket.send(reply)
# start_server = websockets.serve(handler, "localhost", 8765)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()


# async def handler(websocket):
#     while True:
#         try:
#             message = await websocket.recv()
#         except websockets.ConnectionClosedOK:
#             break
#         print(message)


async def handler(websocket):
    async for message in websocket:
        reply = f"Data recieved as:  {message}!"
        print(reply)
        await websocket.send(reply)


async def main():
    async with websockets.serve(handler, "", 8765):  # async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())


# cd venv\Scripts
# activate
# cd ..

# pip install --upgrade pip
# pip install ccxt
# pip install websockets
# pip install websocket-client
# pip install websocket-server

# pip freeze > requirements.txt
# pip install -r requirements.txt
