from loguru import logger
import time
import datetime as dt
import asyncio
from pyinstrument import Profiler
import pyinstrument


async def teste():
    p = Profiler(async_mode='disabled')

    with p:
        print('Hello ...')
        await asyncio.sleep(1)
        print('... World!')

    p.print()


def main():
    start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time() # time.monotonic()
    logger.info(f'Inicio') 
    try:

        # asyncio.run(teste())

        profiler = pyinstrument.Profiler()
        with profiler:
            time.sleep(1) # do some work here...
        print(profiler.output_text())

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()  # time.monotonic()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    # logger.add("file_{time}.log", level='DEBUG', rotation="500 MB", compression="zip", enqueue=True, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    main()

# python -m pip install --upgrade pyinstrument

# python main.py
# python pyinstrument --renderer=json main.py