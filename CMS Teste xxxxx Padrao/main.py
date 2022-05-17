from loguru import logger
import time
import datetime as dt
import functools
import sys 
import os
from dynaconf import Dynaconf
from dotenv import load_dotenv, find_dotenv


def config_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        end_time   = start_time - start_time
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f'{func.__name__}.inicio - params: {signature}')  #if signature: logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()
            result = func(*args, **kwargs)
            end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
            return result
        except Exception as e:
            logger.error(f'{func.__name__}.erro: "{str(e)}"')
            # logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
        finally:
            logger.info(f'{func.__name__}.fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}')

    return wrapper


@config_log
def config_env():
    # logger.info(f'inicio')
    try:

        # environment variables

        # load_dotenv(find_dotenv()) # os.getenv("CMS_DOMAIN")
        settings = Dynaconf(load_dotenv=True, environments=True, envvar_prefix="CMS")
        logger.debug(f'{settings.DOMAIN=}') 
        logger.debug(f'{settings["DOMAIN"]=}') 

    except Exception as e:
        raise # logger.error(f'Falha Geral(main): "{str(e)}"')
    finally:
        pass # logger.info(f'fim')


def teste_01_xxx():
    try:

        result = 'ok'
        logger.info(f'{result=}') 

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time() # time.monotonic()
    logger.info(f'Inicio') 
    try:

        config_env()

        # teste_01_xxx()

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()  # time.monotonic()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    # logger.add("file_{time}.log", level='DEBUG', rotation="500 MB", compression="zip", enqueue=True, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade xxxxxxx
# python -m pip install --upgrade pip
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
# python3 main.py  
# pypy3 main.py
