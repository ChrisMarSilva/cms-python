import asyncio
import datetime as dt
import time

import httpx
from loguru import logger


async def fetch_store(client, url):
    resp = await client.get(url)
    products = resp.json()
    return url, products["products"][0]["title"]


async def teste_01():
    with open("stores.txt", "r") as f:
        urls = [line.strip() for line in f.readlines()]
    async with httpx.AsyncClient() as client:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(fetch_store(client, url)))
        results = await asyncio.gather(*tasks)
    return results


def main():
    try:

        logger.info(f"Inicio")
        start_time = time.perf_counter()

        results = asyncio.run(teste_01())
        logger.info(results)

        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == "__main__":
    main()

# python -m pip install --upgrade httpx
# python -m pip install --upgrade flake8
# python -m pip install --upgrade black
# python -m pip install --upgrade mypy
# python -m pip install --upgrade pylint
# python -m pip install --upgrade bandit
# python -m pip install --upgrade pydocstyle


# python main.py
# python -m black main.py
# python -m mypy main.py
# python -m pylint main.py
# python -m bandit main.py
# python -m pydocstyle test_main.py
