from loguru import logger
import datetime as dt
import time
import json
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        with open("config.json") as json_data_file:
            data = json.load(json_data_file)
        
        logger.info(data)
        logger.info(data['mysql'])
        logger.info(data['mysql']['host'])

        outfile = {
            "mysql": {
                "db": "write-math",
                "host": "localhost",
                "passwd": "my secret password",
                "user": "root",
            },
            "other": {
                "preprocessing_queue": [
                    "preprocessing.scale_and_center",
                    "preprocessing.dot_reduction",
                    "preprocessing.connect_lines",
                ],
                "use_anonymous": True,
            },
        }

        with open("config2.json", "w") as outfile:
            json.dump(data, outfile)

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
