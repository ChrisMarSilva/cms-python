from loguru import logger
import datetime as dt
import time
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        with open("config.xml") as f:
            content = f.read()

        soup = BeautifulSoup(markup=content, features='lxml')
        logger.info(f'{soup.mysql.host.contents[0]=}')

        for tag in soup.other.preprocessing_queue:
            if str(tag) == '\n': continue
            logger.info(f'{tag=}')

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade BeautifulSoup
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
