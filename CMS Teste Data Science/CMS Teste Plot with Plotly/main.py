from loguru import logger
import datetime as dt
import time
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from dotenv import load_dotenv


def teste_01_xxx():
    try:

        result = 'ok'
        logger.info(f'{result=}') 

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        teste_01_xxx()
        
        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade seaborn 
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
