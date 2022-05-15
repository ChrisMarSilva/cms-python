from loguru import logger
import time
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        pass

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s")

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
# python3 main.py  
# pypy3 main.py
