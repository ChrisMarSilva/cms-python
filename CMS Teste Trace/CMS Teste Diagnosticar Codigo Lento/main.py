import requests
import httpx
import aiohttp
import asyncio
import time
import cProfile
import pstats
import platform
from dotenv import load_dotenv


url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey=<apikey>'
symbols = ['AAPL', 'GOOG', 'TSLA', 'MSFT']


def count_https_in_web_pages():
    htmls = []
    for symbol in symbols:
        htmls.append(requests.get(url=url.format(symbol)).json())
    print(f'len {len(htmls)}')


async def count_https_in_web_pages_better():
    htmls = []
    async with httpx.AsyncClient() as client:
        tasks = (client.get(url.format(symbol)) for symbol in symbols)
        reqs = await asyncio.gather(*tasks)
        htmls = [req.json() for req in reqs]
    print(f'len {len(htmls)}')


def main():

    if platform.system()=='Windows':
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    start = time.perf_counter()

    with cProfile.Profile() as pr:
        # count_https_in_web_pages()                    # done in 1.91s
        asyncio.run(count_https_in_web_pages_better())  # done in 0.59s 
        
    elapsed = time.perf_counter() - start
    print(f'done in {elapsed:.2f}s ')

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename='needs_profiling.prof')



if __name__ == '__main__':
    main()


# py -3 -m venv .venv

# python -m pip install psutil
# python -m pip install snakeviz
# python -m pip install httpx

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste Diagnosticar Codigo Lento
# .venv\scripts\activate
# python main.py
# snakeviz ./needs_profiling.prof
