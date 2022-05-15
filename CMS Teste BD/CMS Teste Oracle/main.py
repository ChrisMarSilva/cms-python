from loguru import logger
import time
import datetime as dt
import cx_Oracle
from dotenv import load_dotenv


def teste_01_xxx():
    try:

        connection = cx_Oracle.connect(user="hr", password="welcome", dsn="localhost/orclpdb1")
        # connection = cx_Oracle.connect(uid+"/"+pwd+"@"+db) #cria a conexão

        cursor = connection.cursor()

        sql = """ SELECT first_name, last_name FROM employees WHERE department_id = :did AND employee_id > :eid"""
        cursor.execute(sql, did = 50, eid = 190)
        for fname, lname in cursor:
            logger.info(f'Values: {fname} - {lname}') 

        cursor.execute("SELECT * from tab") # consulta sql
        result = cursor.fetchone()  # busca o resultado da consulta
        if result == None: 
                print("Nenhum Resultado")

        cursor.close()
        connection.close()

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
# python -m pip install --upgrade cx_Oracle 
# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py
# python3 main.py  
# pypy3 main.py
