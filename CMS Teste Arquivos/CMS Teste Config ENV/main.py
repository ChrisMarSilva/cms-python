from loguru import logger
import datetime as dt
import time
import os
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        load_dotenv() # To work with the .env file

        api_key = os.getenv('ALPHAVANTAGE_API_KEY')
        logger.info(f'{api_key=}') 

# from os import getenv
# from dotenv import load_dotenv
# from os.path import dirname, isfile, join




# _ENV_FILE = join(dirname(__file__), '.env_')
# if isfile(_ENV_FILE):
#     load_dotenv(dotenv_path=_ENV_FILE)





        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade xxxxxxx
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
