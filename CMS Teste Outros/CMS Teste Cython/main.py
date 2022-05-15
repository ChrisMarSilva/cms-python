from re import A
from loguru import logger
import datetime as dt
import time
from timeit import timeit
import pyximport; pyximport.install()
# import fib_py
import fib_cy
import fib_x
import c_fib_import
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # ----------------------------------------------------------

        # n = 100_000  # 100_000  # 1_000_000

        # start = time.perf_counter()
        # fib_py.fib(n=n)
        # endt = time.perf_counter() - start
        # logger.info(f'fib in py - Done in {endt:.2f}s - {dt.timedelta(seconds=endt)}') # 15.23s - 0:00:15.231507

        # start = time.perf_counter()
        # fib_cy.fib(n=n)
        # endt = time.perf_counter() - start
        # logger.info(f'fib in cy - Done in {endt:.2f}s - {dt.timedelta(seconds=endt)}') # 18.28s - 0:00:18.283626

        # start = time.perf_counter()
        # fib_x.fib(n)
        # endt = time.perf_counter() - start
        # logger.info(f'fib in pyx - Done in {endt:.2f}s - {dt.timedelta(seconds=endt)}') # 0.00s - 0:00:00.000688

        # ----------------------------------------------------------
        # ----------------------------------------------------------

        num = 1_000_000  # 100_000  # 1_000_000

        py = timeit('fib(93)', number=num, setup='from fib_py import fib')
        cy = timeit('fib(93)', number=num, setup='from fib_cy import fib')
        px = timeit('fib(93)', number=num, setup='from fib_x import fib')
        cc = timeit('fib(93)', number=num, setup='from c_fib_import import fib')

        logger.info(f'')
        logger.info(f'Python Puro: {py:.2f}s')    # 10.67s
        logger.info(f'Cython/Python: {cy:.2f}s')  #  0.20s
        logger.info(f'Cython Puro: {px:.2f}s')    #  0.15s
        logger.info(f'C Puro: {cc:.2f}s')         #  0.22s
        logger.info(f'')
        logger.info(f'{py/cy=}')
        logger.info(f'{py/px=}')
        logger.info(f'{py/cc=}')
        logger.info(f'{cy/cc=}')
        logger.info(f'{px/cc=}')
        logger.info(f'')

        # ----------------------------------------------------------

        # from random import randint
        # from fib_cy import fib
        # numeros = [randint(0, 93) for _ in range(100_000)]
        # for n in numeros:
        #     fib(n)

        # ----------------------------------------------------------

        # import hw
        # hw.show("ccccccccc")
        # hw.show_all(["aaa", "bbb", "ccc"])

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade numpy
# python -m pip install --upgrade oursql
# python -m pip install --upgrade cython
# python -m pip install --upgrade easycython
# python -m pip install --upgrade setuptools-cythonize
# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py

