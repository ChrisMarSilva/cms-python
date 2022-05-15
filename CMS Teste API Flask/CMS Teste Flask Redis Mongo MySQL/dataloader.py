from loguru import logger
import datetime as dt
import time
import json
import requests


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        with open('./people.json', encoding='utf-8') as f:
            people = json.loads(f.read())

        for person in people:
            # logger.info(f"Person {person['first_name']} {person['last_name']} ")
            try:
                r = requests.post('http://127.0.0.1:5001/person/new', json=person)
                if r.status_code == 200:
                    logger.info(f" --> Created person {person['first_name']} {person['last_name']} with ID {r.text}")
                else:
                    logger.error(f" --> person {person['first_name']} {person['last_name']} - Erro: {r.text}")
            except Exception as e:
                logger.error(e)
            # break

        # cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API Flask\CMS Teste Flask RedisFlask"
        # python dataloader.py

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

# python dataloader.py
