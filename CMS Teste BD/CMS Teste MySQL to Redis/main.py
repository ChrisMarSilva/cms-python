from loguru import logger
import time
import datetime as dt
import pymysql
import pymysql.cursors
import uuid
import redis
import json
import base64
from dotenv import load_dotenv


def teste_mysql_to_redis():
    try:

        r = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
        # r = redis.from_url('redis://foo.bar.com:12345')
        r.ping()
        
        start_time = time.perf_counter()
        r.flushdb()
        # for name in r.keys():
        #     r.delete(name) # for k in r.hkeys(name=name): r.hdel(name, k)
        end_time = time.perf_counter() - start_time 
        logger.info(f"Limpar Redis - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        connection = pymysql.connect(host="localhost", user="root", password="password", database="database", cursorclass=pymysql.cursors.DictCursor) 
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, SITE, DTHRREGISTRO, TIPO, TITULO, LINK, SITUACAO FROM TBALERTA_NOTICIA ORDER BY ID")
                result = cursor.fetchall()
                logger.info(f'noticias={len(result)}') 

                start_time = time.perf_counter()
                for row in result:
                    key = str(uuid.uuid4().hex).upper()
                    value = row  # {"first_name": "Robert", "last_name": "McDonald", "age": 35}
                    r.hset(name=f"noticia:{key}", mapping=value)
                end_time = time.perf_counter() - start_time 
                logger.info(f"Popular Redis - noticia - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

                cursor.execute("SELECT ID, NOME, EMAIL, SENHA, DTREGISTRO, TENTATIVA, TIPO, SITUACAO, FOTO, CHATID FROM TBUSUARIO ORDER BY ID")
                result = cursor.fetchall()
                logger.info(f'usuarios={len(result)}') 

                start_time = time.perf_counter()
                for row in result:
                    key = str(row["EMAIL"]).upper()  # str(uuid.uuid4().hex).upper()
                    # key = base64.b64encode(key.encode()).decode()  # str(base64.b64decode(key).decode())
                    value = row
                    value = {key:val for key, val in value.items() if val and str(val) != ""}
                    r.hset(name=f"usuario:{key}", mapping=value)
                    # break
                end_time = time.perf_counter() - start_time 
                logger.info(f"Popular Redis - usuarios - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        teste_mysql_to_redis()

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
# python -m pip install --upgrade mysql-connector-python
# python -m pip install --upgrade PyMySQL
# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py
