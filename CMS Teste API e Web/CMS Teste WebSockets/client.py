#!/usr/bin/env python
import asyncio
import websockets


async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()


if __name__ == '__main__':
    asyncio.run(hello())
