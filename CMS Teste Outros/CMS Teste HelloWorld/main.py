from loguru import logger
import time
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        minha_variavel:  int = 1
        logger.info(f'minha_variavel: {minha_variavel} - {type(minha_variavel)}')
        minha_variavel = "CMS"
        logger.info(f'minha_variavel: {minha_variavel} - {type(minha_variavel)}')

        total = 0
        for i in range(1, 10000): # 10.000
            for j in range(1, 10000): # 10.000
                total += i + j

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()
# py -3 -m venv .venv

# python -m pip install --upgrade psutil

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate

# python main.py
# The result is 999800010000 - It took 13.85 seconds to compute
# The result is 999800010000 - It took 14.66 seconds to compute

# python3 main.py  
# The result is 999800010000 - It took 0.30 seconds to compute
# The result is 999800010000 - It took 0.27 seconds to compute

# pypy3 main.py
# The result is 999800010000 - It took 0.27 seconds to compute
# The result is 999800010000 - It took 0.31 seconds to compute

