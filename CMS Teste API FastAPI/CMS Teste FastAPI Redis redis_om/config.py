from redis_om import get_redis_connection
import os


# https://pypi.org/project/redis-om/


# os.environ["REDIS_OM_URL"] = "redis://default:123@localhost:6379/0" # redis://default:<password>@<host>:<port>
# URL = os.environ.get("REDIS_OM_URL", None)
# print('REDIS_OM_URL', URL)


# redis_db = get_redis_connection()
# redis_db = get_redis_connection(url=URL)
redis_db =  get_redis_connection(host='localhost', port=6379, db=0, password='123', charset='utf-8', decode_responses=True)
# print('redis_db', redis_db)
