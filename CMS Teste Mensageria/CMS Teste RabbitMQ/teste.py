



# import asyncio
#
# async def main():
#     print('Hello ...')
#     await asyncio.sleep(1)
#     print('... World!')
#
# # Python 3.7+
# asyncio.run(main())
#
#
#
# import asyncio
# import time
#
# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)
#
# async def main():
#     print(f"started at {time.strftime('%X')}")
#
#     await say_after(1, 'hello')
#     await say_after(2, 'world')
#
#     print(f"finished at {time.strftime('%X')}")
#
# asyncio.run(main())
#
#
#
# async def main():
#     task1 = asyncio.create_task(
#         say_after(1, 'hello'))
#
#     task2 = asyncio.create_task(
#         say_after(2, 'world'))
#
#     print(f"started at {time.strftime('%X')}")
#
#     # Wait until both tasks are completed (should take
#     # around 2 seconds.)
#     await task1
#     await task2
#
#     print(f"finished at {time.strftime('%X')}")
#
#
# lock = asyncio.Lock()
#
# # ... later
# await lock.acquire()
# try:
# # access shared state
# finally:
#     lock.release()
#
#
# lock = asyncio.Lock()
#
# # ... later
# async with lock:
#     # access shared state
#
#     loop = asyncio.get_event_loop()
# tasks = [my_coroutine(term) for term in terms]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()
#
#
# import asyncio
# import random
#
# @asyncio.coroutine
# def my_coroutine(term):
#     print("start", term)
#     yield from asyncio.sleep(random.uniform(1, 3))
#     print("end", term)
#
#
# terms = ["pie", "chicken", "things", "stuff"]
# loop = asyncio.get_event_loop()
# tasks = [my_coroutine(term) for term in terms]
# print("Here we go!")
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()
#
# import asyncio
#
# async def coro(term):
#     for i in range(3):
#         await asyncio.sleep(int(len(term)))  # just sleep
#         print("cor1", i, term)
#
# terms = ["pie", "chicken", "things", "stuff"]
# tasks = [coro(term) for term in terms]
#
# loop = asyncio.get_event_loop()
# cors = asyncio.wait(tasks)
# loop.run_until_complete(cors)
#
#
# mport asyncio
#
# async def myWorker():
#     print("Hello World")
#
# async def main():
#     print("My Main")
#
# try:
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.wait([myWorker() for i in range(5)], timeout=2))
# except KeyboardInterrupt:
#     pass
# finally:
#     loop.close()
#
#
#
# async def myWorker():
#     print("Hello World")
#
# async def main():
#     print("My Main")
#
# try:
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(*[myWorker() for i in range(5)]))
# except KeyboardInterrupt:
#     pass
# finally:
#     loop.close()
#
#
#     import asyncio
#
# async def myWorker(number):
#     return number * 2
#
# async def main(coros):
#     for fs in asyncio.as_completed(coros):
#         print(await fs)
#
# coros = [myWorker(1) for i in range(5)]
#
# try:
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main(coros))
# except KeyboardInterrupt:
#     pass
# finally:
#     loop.close()
#
