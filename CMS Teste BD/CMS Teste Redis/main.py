from loguru import logger
import time
import redis
import json
import datetime
import pymysql
import pymysql.cursors
from pprint import pprint
from dynaconf import Dynaconf
from dotenv import load_dotenv, find_dotenv


def teste_01_connection() -> redis.Redis:
    r = redis.Redis(host='localhost', port=6379, db=0, password='123')
    # r = redis.Redis(password='123')
    # pool = redis.ConnectionPool(host='localhost', port=6379, db=0, password='123', charset='utf-8', decode_responses=True)
    # r = redis.Redis(connection_pool=pool)
    # r = redis.StrictRedis(host='localhost', port=6379, db=0, password='123')
    return r


def teste_02_set_get(r: redis.Redis) -> None:
    r.set(name='foo0', value='bar0')
    r.set(name='foo1', value='bar1')
    r.set(name='foo2', value='bar2')
    r.set(name='foo3', value='bar3')
    logger.info(f"#1: {r.get(name='foo0')=}")
    logger.info(f"#1: {r.get(name='foo9')=}")


def teste_03_rpush_lrange(r: redis.Redis) -> None:
    r.rpush('ferramentas', 'martelo')
    r.rpush('ferramentas', 'serrote')
    r.rpush('ferramentas', 'machado')
    logger.info(f"#2: {r.lrange(name='ferammentas', start=0, end=-1)}")
    logger.info(f"#2: {r.llen(name='ferramentas')}")
    logger.info(f"#2: {r.lindex(name='ferramentas', index=1)}")
    r.delete('ferramentas')
    logger.info('#2' , r.lrange(name='ferammentas', start=0, end=-1))


def teste_04_sadd_zadd_zrange(r: redis.Redis) -> None:

    #logger.info(f"#3: {r.sadd('ferramentas', 'martelo')}")
    #logger.info(f"#3: {r.sadd('ferramentas', 'serrote')}")
    #logger.info(f"#3: {r.sadd('ferramentas', 'machado')}")
    #logger.info(f"#3: {r.sadd('ferramentas', 'martelo')}")
    # logger.info(f"#3: {r.smembers('ferramentas')}")

    # r.zadd('test:scores', 'testid:9000', 50)
    # r.zadd('test:scores', 'testid:8000', 20)
    # r.zadd('test:scores', 'testid:7000', 45)
    #r.zadd('test:scores', 'testid:7000', 45)
    #r.zrange('test:scores', 0, -1, withscores=True)

    test = r.zrange(name='test:scores', start=0, end=-1, withscores=True)
    test.reverse()


def teste_05_mset_get(r: redis.Redis) -> None:
    r.mset(mapping={"Croatia": "Zagreb", "Bahamas": "Nassau"})
    r.get(name="Bahamas")


def teste_06_smembers_scard(r: redis.Redis) -> None:
    today = datetime.date.today()
    stoday = today.isoformat()
    r.sadd(name=stoday, values={"dan", "jon", "alex"})
    logger.info(r.smembers(name=stoday))
    logger.info(r.scard(name=today.isoformat()))


def teste_07_hincrby_hget(r: redis.Redis) -> None:
    r.hincrby(name="hat:56854717", key="quantity", amount=-1)
    logger.info(r.hget(name="hat:56854717", key="quantity"))
    r.hincrby(name="hat:56854717", key="npurchased", amount=1)
    logger.info(r.hget(name="hat:56854717", key="npurchased"))


def teste_08_lpush(r: redis.Redis) -> None:
    r.lpush(name="ips", values="51.218.112.236")
    r.lpush(name="ips", values="90.213.45.98")
    r.lpush(name="ips", values="115.215.230.176")
    r.lpush(name="ips", values="51.218.112.236")

def teste_09_hset(r: redis.Redis) -> None:
    r.hset("mykey", "field1", "value1")

def teste_10_json(r: redis.Redis):
    restaurant_484272 = {"name": "Ravagh","type": "Persian","address": {"street": {"line1": "11 E 30th St","line2": "APT 1",},"city": "New York","state": "NY","zip": 10016,}}
    r.set(484272, json.dumps(restaurant_484272))
    pprint(json.loads(r.get(484272)))

def teste_11_pipeline_sadd(r: redis.Redis):
    r.set('bing', 'baz')
    pipe = r.pipeline()
    pipe.set('foo', 'bar')
    pipe.get('bing')
    logger.info(pipe.execute())
    pipe.set('foo', 'bar').sadd('faz', 'baz').incr('auto_number').execute()

def teste_12_pipeline_multi(r: redis.Redis) -> None:
    # pipe = r.pipeline(transaction=False)
    # with r.pipeline() as pipe:
    #     while True:
    #         try:
    #             # put a WATCH on the key that holds our sequence value
    #             pipe.watch('OUR-SEQUENCE-KEY')
    #             # after WATCHing, the pipeline is put into immediate execution
    #             # mode until we tell it to start buffering commands again.
    #             # this allows us to get the current value of our sequence
    #             current_value = pipe.get('OUR-SEQUENCE-KEY')
    #             next_value = int(current_value) + 1
    #             # now we can put the pipeline back into buffered mode with MULTI
    #             pipe.multi()
    #             pipe.set('OUR-SEQUENCE-KEY', next_value)
    #             # and finally, execute the pipeline (the set command)
    #             pipe.execute()
    #             # if a WatchError wasn't raised during execution, everything
    #             # we just did happened atomically.
    #             break
    #         except Exception:
    #             # another client must have changed 'OUR-SEQUENCE-KEY' between
    #             # the time we started WATCHing it and the pipeline's execution.
    #             # our best bet is to just retry.
    #             continue
    pass

def teste_13_pipeline_watch(r: redis.Redis) -> None:
    pipe = r.pipeline()
    while True:
        try:
            pipe.watch('foo')
            logger.info(pipe.execute())
            break
        except: # WatchError:
            continue
        finally:
            pipe.reset()

def teste_14_lock(r: redis.Redis) -> None:
    try:
        with r.lock('my-lock-key', blocking_timeout=5) as lock:
            logger.info(f'ok 1')  # code you want executed only after the lock has been acquired
            try:
                with r.lock('my-lock-key', blocking_timeout=5) as lock:
                    logger.info(f'ok 2') # code you want executed only after the lock has been acquired
            except Exception:
                logger.info(f'Erro 2')  # the lock wasn't acquired
    except Exception:  # LockError:
        logger.info(f'Erro 1')  # the lock wasn't acquired

def teste_07_xxx(r: redis.Redis) -> None:
    pass


def teste_99_performace_mysql_redis(r: redis.Redis) -> None:
    try:

        settings = Dynaconf(load_dotenv=True, environments=True, envvar_prefix="CMS_TNB")
        mysql_host, mysql_user, mysql_password, mysql_database = settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASS, settings.MYSQL_DB
        logger.info(f'MYSQL   = {mysql_host} - {mysql_user} - {mysql_password} - {mysql_database}')

        connection = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:

                # CREATE TABLE TBTESTE_PESSOA ( ID int(11) NOT NULL, NOME varchar(100) NOT NULL, SITUACAO varchar(1) NOT NULL, PRIMARY KEY (ID) ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

                # cursor.execute("TRUNCATE TABLE TBTESTE_PESSOA")
                # connection.commit()

                # params = [(idx+1, f'Pessoa {idx+1}', 'A') for idx in range(10_000)]  # 10_000 # 1_000_000
                # # logger.info(f"{params}") 

                # sql = "INSERT INTO TBTESTE_PESSOA (ID, NOME, SITUACAO) VALUES (%s, %s, %s)"
                # cursor.executemany(sql, params)
                # connection.commit()

                # -------------------------------------------------------------------
                # -------------------------------------------------------------------

                # Teste 1 - fazer Duas consultas na Base MySQL para cada ID

                # cursor.execute("SELECT ID, NOME, SITUACAO FROM TBTESTE_PESSOA")
                # result = cursor.fetchall()

                # start_time = time.perf_counter() 

                # for row in result:
                #     # logger.info(f"{row['NOME']}") 

                #     cursor.execute("SELECT ID, NOME, SITUACAO FROM TBTESTE_PESSOA WHERE ID = %s", (row['ID'], ))
                #     novo_result = cursor.fetchone()
                #     # logger.info(f"ID:{row['ID']} - Consulta #1: {novo_result['NOME']}") 

                #     cursor.execute("SELECT ID, NOME, SITUACAO FROM TBTESTE_PESSOA WHERE ID = %s", (row['ID'], ))
                #     novo_result = cursor.fetchone()
                #     # logger.info(f"ID:{row['ID']} - Consulta #2: {novo_result['NOME']}") 

                # end_time = time.perf_counter() - start_time 
                # logger.info(f"MySQL + MySQL - Done in {end_time:.2f}s")

                # -------------------------------------------------------------------
                # -------------------------------------------------------------------

                # Teste 2 - fazer Duas consultas na Base MySQL para cada ID

                cursor.execute("SELECT ID, NOME, SITUACAO FROM TBTESTE_PESSOA")
                result = cursor.fetchall()

                start_time = time.perf_counter() 

                for row in result:
                    # logger.info(f"{row['NOME']}") 

                    key = "Pessoa-Id-" + str(row['ID'])

                    novo_result_redis = r.get(name=key)
                    # logger.info(f"{novo_result_redis=}") 

                    if not novo_result_redis:
                        cursor.execute("SELECT ID, NOME, SITUACAO FROM TBTESTE_PESSOA WHERE ID = %s", (row['ID'], ))
                        novo_result_mysql = cursor.fetchone()
                        # logger.info(f"ID:{row['ID']} - Consulta #1: {novo_result_mysql['NOME']}") 

                        r.set(name=key, value=json.dumps(novo_result_mysql))

                    novo_result_redis = r.get(name=key)
                    # logger.info(f"{novo_result_redis=}") 

                end_time = time.perf_counter() - start_time 
                logger.info(f"MySQL + Redis - Done in {end_time:.2f}s")

                # -------------------------------------------------------------------
                # -------------------------------------------------------------------

                # MySQL + MySQL - Done in 42.34s
                # MySQL + Redis - Done in 75.67s
                # MySQL + Redis - Done in 46.62s
                # MySQL + Redis - Done in 36.45s

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')



def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        r = teste_01_connection()
        # teste_02_set_get(r=r)
        # teste_03_rpush_lrange(r=r)
        # teste_04_sadd_zadd_zrange(r=r)
        # teste_05_mset_get(r=r)
        # teste_06_smembers_scard(r=r)
        # teste_07_hincrby_hget(r=r)
        # teste_08_lpush(r=r)
        # teste_09_hset(r=r)
        # teste_10_json(r=r)
        # teste_11_pipeline_sadd(r=r)
        # teste_12_pipeline_multi(r=r)
        # teste_13_pipeline_watch(r=r)
        # teste_14_lock(r=r)
        # teste_99_performace_mysql_redis(r=r)
        
        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s")

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade redis
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
