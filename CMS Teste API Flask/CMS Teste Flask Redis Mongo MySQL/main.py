from flask import Flask, request, render_template, make_response
import json
from loguru import logger
# from config import redis_client
import uuid
import time
import datetime as dt
import logging


app = Flask(import_name=__name__.split('.')[0], template_folder='') 
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
# redis_client.init_app(app=app)

from flask_cors import CORS
CORS(app)  # CORS(app, resources={r"*": {"origins": "*"}})

# class InterceptHandler(logging.Handler):
#     def emit(self, record):
#         logger_opt = logger.opt(depth=6, exception=record.exc_info)
#         logger_opt.log(record.levelno, record.getMessage())
# logger.start("log.log", level='DEBUG', format="{time} {level} {message}", backtrace=True, rotation='25 MB')
# app.logger.addHandler(InterceptHandler())



@app.route("/", methods=["GET"])
def home():
    try:

        import pymysql
        import pymysql.cursors
        connection = pymysql.connect(host="localhost", user="root", password="password", database="database", cursorclass=pymysql.cursors.DictCursor) 

        import redis
        redis_client = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

        from pymongo import MongoClient
        client = MongoClient(host='mongodb://root:example@localhost:27017/?maxPoolSize=20&retryWrites=true&w=majority', serverSelectionTimeoutMS=1000) 
        db = client["test-database-py-flask"]

        with connection:
            with connection.cursor() as cursor:

                start_time = time.perf_counter()
                noticias = []
                cursor.execute("SELECT ID, SITE, DTHRREGISTRO, TIPO, TITULO, LINK, SITUACAO FROM TBALERTA_NOTICIA ORDER BY ID")
                result = cursor.fetchall()
                noticias = [row for row in result]
                end_time = time.perf_counter() - start_time 
                end_time_mysql_notic = f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}"
                logger.info(f"Carregar MySQL - noticia - Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

                start_time = time.perf_counter()
                nome_user, user_user = "", ""
                cursor.execute("SELECT ID, NOME, EMAIL, SENHA, DTREGISTRO, TENTATIVA, TIPO, SITUACAO, FOTO, CHATID FROM TBUSUARIO WHERE EMAIL = 'marcomatav@hotmail.com' OR EMAIL LIKE 'marcomatav@%' ")
                result = cursor.fetchone()
                nome_user, user_user = result['NOME'], result['EMAIL']
                end_time = time.perf_counter() - start_time 
                end_time_mysql_user = f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}"
                logger.info(f"Carregar MySQL - usuario - Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        start_time = time.perf_counter()
        noticias = []
        for key in redis_client.keys():
            row = redis_client.hgetall(name=key)
            # for k, v in row.items(): logger.info("k", k.decode('utf-8')) 
            # noticias.append({"ID": row[b'ID'].decode('utf-8'), "SITE": row[b'SITE'].decode('utf-8'), "DTHRREGISTRO": row[b'DTHRREGISTRO'].decode('utf-8'), "TIPO": row[b'TIPO'].decode('utf-8'), "TITULO": row[b'TITULO'].decode('utf-8'), "LINK": row[b'LINK'].decode('utf-8'),  "SITUACAO": row[b'SITUACAO'].decode('utf-8')})
            # noticias.append({"ID": row['ID'], "SITE": row['SITE'], "DTHRREGISTRO": row['DTHRREGISTRO'], "TIPO": row['TIPO'], "TITULO": row['TITULO'], "LINK": row['LINK'],  "SITUACAO": row['SITUACAO']})
        end_time = time.perf_counter() - start_time 
        end_time_redis_notic = f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}"
        logger.info(f"Carregar Redis - noticia - Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        start_time = time.perf_counter()
        nome_user, user_user = "", ""
        result = redis_client.hgetall(name=f"usuario:{str('marcomatav@hotmail.com').upper()}")
        nome_user, user_user = result['NOME'], result['EMAIL']
        end_time = time.perf_counter() - start_time 
        end_time_redis_user = f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}"
        logger.info(f"Carregar Redis - usuario - Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        start_time = time.perf_counter()
        noticias = []
        # for row in db.noticias.find(): noticias.append({"ID": row['ID'], "SITE": row['SITE'], "DTHRREGISTRO": row['DTHRREGISTRO'], "TIPO": row['TIPO'], "TITULO": row['TITULO'], "LINK": row['LINK'],  "SITUACAO": row['SITUACAO']})
        # noticias = [{"ID": row['ID'], "SITE": row['SITE'], "DTHRREGISTRO": row['DTHRREGISTRO'], "TIPO": row['TIPO'], "TITULO": row['TITULO'], "LINK": row['LINK'],  "SITUACAO": row['SITUACAO']} for row in db.noticias.find()]
        noticias = [row for row in db.noticias.find()]
        end_time = time.perf_counter() - start_time 
        end_time_mongodb_notic = f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}"
        logger.info(f"Carregar MongoDB - noticia - Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        start_time = time.perf_counter()
        nome_user, user_user = "", ""
        result = db.usuarios.find_one({"EMAIL": 'marcomatav@hotmail.com'})
        nome_user, user_user = result['NOME'], result['EMAIL']
        end_time = time.perf_counter() - start_time 
        end_time_mongodb_user = f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}"
        logger.info(f"Carregar MongoDB - usuario - Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        # python main.py

        data = {"data": {"usuario": {"nome": nome_user, "email": user_user, "end_time_mysql": end_time_mysql_user, "end_time_redis": end_time_redis_user, "end_time_mongodb": end_time_mongodb_user }, "noticia": {"lista": noticias, "end_time_mysql": end_time_mysql_notic, "end_time_redis": end_time_redis_notic, "end_time_mongodb": end_time_mongodb_notic}}}
        return render_template("index.html", **data)  

    except Exception as e:
        logger.error(e)
        data = {"data": {"usuario": {"nome": "", "email": "", "end_time_mysql": "", "end_time_redis": "", "end_time_mongodb": ""}, "noticia": {"lista": [], "end_time_mysql": "", "end_time_redis": "", "end_time_mongodb": ""}}}
        return render_template("index.html", **data)


@app.route("/person/new", methods=["POST"])
def create_person():
    try:

        import redis
        redis_client = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

        key = str(uuid.uuid4().hex).upper()
        # value = request.json
        value = {"first_name": "Robert", "last_name": "McDonald", "age": 35, "address":  "Main Street", "skills": "guitar", "personal_statement": "My name is Robert, I love meeting new people and enjoy music, coding and walking my dog." }
        redis_client.hmset(f"noticia:{key}", value)

        return make_response(json.dumps(key), 200)

    except Exception as e:
        logger.error(e)
        return str(e), 400



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=True)



# py -3 -m venv .venv
# python -m pip install --upgrade flask-redis
# python -m pip install --upgrade pickle
# python -m pip install --upgrade flask-cors
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
