from loguru import logger
import time
import datetime as dt
import os
from math import ceil  # floor
from dynaconf import Dynaconf
from dotenv import load_dotenv, find_dotenv
import pymysql
import pymysql.cursors
from pymysql import converters
import pymongo
from pymongo import MongoClient
from pymongo import UpdateOne, UpdateMany
from decimal import Decimal
from bson.decimal128 import Decimal128
from bson.objectid import ObjectId
import numpy as np
import uuid


def convert_decimal(dict_item):
    # This function iterates a dictionary looking for types of Decimal and converts them to Decimal128
    # Embedded dictionaries and lists are called recursively.
    if dict_item is None: return None

    for k, v in list(dict_item.items()):
        if isinstance(v, dict):
            convert_decimal(v)
        elif isinstance(v, list):
            for l in v:
                convert_decimal(l)
        elif isinstance(v, Decimal):
            dict_item[k] = Decimal128(str(float(v)))  # Decimal128(str(v))

    return dict_item

def correct_encoding(dictionary):
    """Correct the encoding of python dictionaries so they can be encoded to mongodb
    inputs
    -------
    dictionary : dictionary instance to add as document
    output
    -------
    new : new dictionary with (hopefully) corrected encodings"""

    new = {}
    for key1, val1 in dictionary.items():
        # Nested dictionaries
        if isinstance(val1, dict):
            val1 = correct_encoding(val1)

        if isinstance(val1, np.bool_):
            val1 = bool(val1)

        if isinstance(val1, np.int64):
            val1 = int(val1)

        if isinstance(val1, np.float64):
            val1 = float(val1)

        new[key1] = val1

    return new

def get_connection_mysql(mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str) -> pymysql.connections.Connection: 
    # connection = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database, cursorclass=pymysql.cursors.DictCursor)
    converions = converters.conversions
    converions[pymysql.FIELD_TYPE.BIT] = lambda x: '0' if x == '\x00' else '1'
    connection = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database, cursorclass=pymysql.cursors.DictCursor, charset='utf8', conv=converions)
    return connection

def get_client(mongo_uri: str) -> pymongo.MongoClient: 
    client = MongoClient(host=mongo_uri, serverSelectionTimeoutMS=1000)
    return client

def get_database(client: pymongo.MongoClient) -> pymongo.database.Database: 
    db = client["tamonabolsa"]
    return db

def get_collection_noticias(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.noticias
    return collection

def get_collection_admin_log_erros(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.admin_log_erros 
    return collection

def get_collection_usuarios(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios
    return collection

def get_collection_usuarios_config(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_config 
    return collection

def get_collection_usuarios_log(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_log 
    return collection

def get_collection_usuarios_apuracao(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_apuracao 
    return collection

def get_collection_usuarios_apuracao_calculada(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_apuracao_calculada 
    return collection

def get_collection_usuarios_comentario(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario
    return collection

def get_collection_usuarios_comentario_reacao(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario_reacao
    return collection

def get_collection_usuarios_comentario_denuncia(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario_denuncia
    return collection

def get_collection_usuarios_comentario_alerta(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario_alerta
    return collection

def get_collection_empresa_setor(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_setor
    return collection

def get_collection_empresa_subsetor(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_subsetor
    return collection

def get_collection_empresa_segmento(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_segmento
    return collection

def get_collection_empresa(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa
    return collection

def get_collection_empresa_acao(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_acao
    return collection

def get_collection_empresa_fii(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_fii
    return collection

def get_collection_empresa_etf(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_etf
    return collection

def get_collection_empresa_bdr(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_bdr
    return collection

def get_collection_empresa_cripto(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_cripto
    return collection

def get_collection_empresa_finan(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan
    return collection

def get_collection_empresa_finan_agenda(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_agenda
    return collection

def get_collection_empresa_finan_bpa_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpa_tri
    return collection

def get_collection_empresa_finan_bpa_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpa_ano
    return collection

def get_collection_empresa_finan_bpp_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpp_tri
    return collection

def get_collection_empresa_finan_bpp_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpp_ano
    return collection

def get_collection_empresa_finan_dfc_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dfc_tri
    return collection

def get_collection_empresa_finan_dfc_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dfc_ano
    return collection

def get_collection_empresa_finan_dre_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dre_tri
    return collection

def get_collection_empresa_finan_dre_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dre_ano
    return collection


def teste_performace_pessoa(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        # collection = db.teste
        # collection.drop()
        # lista = [{'nome': f'Pessoa {idx} {uuid.uuid4()}', "date": dt.datetime.utcnow()} for idx in range(1_000_000)]  # 10_000 # 1_000_000
        # logger.warning(f"{len(lista)=}")  # 00:00:07,387
        # collection.insert_many(lista)  # 00:00:27,559
        # result = collection.count_documents({})
        # logger.warning(f'{result=}')  # 0:00:00.907303
        # result = collection.find_one({'_id': ObjectId('627863fad9de27544579b2ad')})
        # logger.warning(f'{result=}')  # 0:00:00.053855
        # result = collection.find_one({'nome': 'Pessoa 999964 8597b09f-8737-4068-afee-094b3b11998c'})
        # result = collection.find_one({'nome': 'Pessoa 999997 492f5700-9cff-4661-a936-c9b12345065a'})
        # logger.warning(f'{result=}')  # 0:00:00.711341 Sem indice # 0:00:00.075180 Com Idice
        # result = collection.find_one({'nome': {"$regex": ".*998997*."}}) # 'Pessoa 137978 1a9f1ca6-95f2-4753-aa57-f99899fdbd68'
        # result = collection.find_one({'nome': {"$regex": "^Pessoa 998997.*"}})  # Pessoa 998997 02eb06bf-2d16-48a9-a78f-9256f0ea9d4a'
        # logger.warning(f'{result=}')  # 0:00:00.046181

        pass

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_noticia(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_noticias(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, SITE, DTHRREGISTRO, TIPO, TITULO, LINK, SITUACAO FROM TBALERTA_NOTICIA ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('DTHRREGISTRO')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_admin_log_erros(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_admin_log_erros(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, DATAHORA, IDUSUARIO, ARQUIVO, LINHA, CODIGO, TEXTO, SITUACAO FROM TBLOGERRO ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('DATAHORA')
            collection.create_index('SITUACAO')
            collection.create_index([('DATAHORA', pymongo.ASCENDING), ('ID', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATAHORA', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, NOME, EMAIL, SENHA, DTREGISTRO, TENTATIVA, TIPO, SITUACAO, FOTO, CHATID FROM TBUSUARIO ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('EMAIL')
            collection.create_index([('ID', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

        # collection = get_collection_usuarios(db=db)
        # start_time = time.perf_counter()
        # email = 'email@gmail.com'
        # # result = collection.find_one({'$or': [{"EMAIL": email}, {"EMAIL": {"$regex": email + "@.*"}}]})
        # result = collection.find({"EMAIL": email}).explain() # executionStats
        # logger.warning(f'{result=}')  
        # for row in result:
        #     logger.warning(f'{row=}')  # 0:00:00.051393

        # rows = collection.find({"ID": {'$ne': int(id_usuario)}, "SITUACAO": 'A'}).limit(3)

        # rows = collection.find({"ID": {'$ne': int(id_usuario)}, "SITUACAO": 'A', "TIPO": tipo_usuario}).limit(3)

        # rows = collection.aggregate(
        #     [
        #         {'$lookup': {'from': 'usuarios_comentario', 'localField': 'ID', 'foreignField': 'IDUSUARIO', 'as': 'COMENTARIO' }}, 
        #         {'$unwind': {'path': "$COMENTARIO", 'preserveNullAndEmptyArrays': True }},
        #         {'$match': {
        #             "$and":[
        #                 {"ID": {'$ne': int(id_usuario)}},
        #                 {"SITUACAO": 'A'},
        #                 {"$or":[{"COMENTARIO.ID": int(id_comentario)}, {"COMENTARIO.IDPAI": int(id_comentario)}]}
        #             ]
        #         }},
        #         {'$project': {'_id' : 0, 'ID' : 1, 'NOME' : 1, 'SITUACAO' : 1 }},
        #         {'$limit': 3},
        #     ]
        # )

        # for row in rows:
        #     # logger.warning(f"{row}")
        #     logger.warning(f"{row['ID']} - {row['NOME']} - {row['EMAIL']}")

        #  tot_registro = collection.count_documents({'TIPO': 'A', 'SITUACAO': 'A'})  
        # logger.warning(f"{tot_registro=}")
        
        # qtde_por_pagina = 10
        # pag_atual = 3
        # pag_total = ceil(tot_registro / qtde_por_pagina)  # calcula o número de páginas arredondando o resultado para cima
        # reg_inicio = (qtde_por_pagina * pag_atual) - qtde_por_pagina  # variavel para calcular o início da visualização com base na página atual
        # logger.warning(f"{reg_inicio=}")

        # # reg_inicio = qtde_por_pagina * (pag_atual - 1)
        # # logger.warning(f"{reg_inicio=}")

        # # rows = collection.find(filter={'TIPO': 'A', 'SITUACAO': 'A'}).sort("DATAHORA", -1).skip(reg_inicio).limit(qtde_por_pagina)  # A-Comentario Princ  # A-Ativo
        
        # # cursor = db['students'].find().skip(skips).limit(page_size)

        # rows = collection.aggregate(
        #     [
        #         {'$match': {'TIPO': 'A', 'SITUACAO': 'A'}}, # A-Comentario Princ  # A-Ativo
        #         {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIO', 'foreignField': 'ID', 'as': 'USER' }}, 
        #         {'$unwind': {'path': "$USER", 'preserveNullAndEmptyArrays': True }},
        #         {'$project': {'_id' : 0, 'ID' : 1, 'IDUSUARIO' : 1, 'TEXTO' : 1, 'DATAHORA' : 1, 'NOME' : "$USER.NOME", 'EMAIL' : "$USER.EMAIL", 'FOTO' : "$USER.FOTO" }},
        #         {'$sort': {"DATAHORA": -1}},
        #         {'$skip': reg_inicio},  
        #         {'$limit': qtde_por_pagina},
        #     ]
        # )

        # for idx, row in enumerate(rows):
        #     logger.warning(f"  -> {row}")
        #     # logger.warning(f"  -> #{idx+1}: {row['IDUSUARIO']} {row['IDUSUARIO']} {row['TEXTO'][:6]}")


    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_config(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_config(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT IDUSUARIO, TIPO, VALOR FROM TBUSUARIO_CONFIG ORDER BY IDUSUARIO, TIPO")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDUSUARIO')
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_log(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_log(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDUSUARIO, DATA, DATAHORA, HOSTIP, HOSTNAME, SITUACAO FROM TBUSUARIO_LOG ORDER BY IDUSUARIO, ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDUSUARIO')
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_apuracao(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_apuracao(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDUSUARIO, TIPO, CATEGORIA, MESANO, VALOR, SITUACAO FROM TBAPURACAO ORDER BY IDUSUARIO, TIPO, CATEGORIA, MESANO, ID")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('IDUSUARIO')
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('MESANO', pymongo.ASCENDING)])

        # result = collection.find({'IDUSUARIO': 2}).sort("MESANO", 1).limit(1) #  SEELCT MIN(ANO_MES) FROM TABELA WHERE IDUSUARIO = 2 LIMIT 1
        # logger.warning(f"{result[0]}") 
        
        # result = collection.find({"IDUSUARIO": 2, "TIPO": 'M', "CATEGORIA": 'C', "MESANO": {"$gte": '202003', "$lte": '202006'}})
        # for row in result:
        #     logger.warning(f"{row}") 

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_apuracao_calculada(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_apuracao_calculada(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDUSUARIO, CATEGORIA, MESANO, VLR_VENDA, VLR_LUCRO_APURADO, VLR_PREJUIZO_COMPENSAR, VLR_BASE_CALCULO, VLR_IR_DEVIDO, VLR_IR_PAGO, VLR_IR_PAGAR FROM TBAPURACAO_CALCULADA ORDER BY IDUSUARIO, CATEGORIA, MESANO, ID")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('IDUSUARIO')
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('MESANO', pymongo.ASCENDING)])

        # apurac = collection.find_one({"IDUSUARIO": 2, "TIPO": 'M', "CATEGORIA": 'C', "MESANO": f'202003'})
        # logger.warning(f"{apurac}") 

        # qtde = collection.count_documents({"IDUSUARIO": 2, "CATEGORIA": 'C', "MESANO": {"$gte": '202312'}})
        # logger.warning(f"{qtde=}") 

        # rows = collection.find({"IDUSUARIO": 2, "CATEGORIA": 'C', "MESANO": {"$gte": '202112'}})
        # rows = collection.find({"IDUSUARIO": 2, "CATEGORIA": 'C', "MESANO": {"$gte": '202201', "$lte": '202205'}})
        # rows = collection.find({"IDUSUARIO": 2, "MESANO": '202205'}).sort([["MESANO", 1], ["CATEGORIA", 1]])
        # for row in rows:
        #     logger.warning(f"{row['MESANO']} - {row['CATEGORIA']}") 

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_comentario(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_comentario(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDPAI, IDUSUARIO, TIPO, TEXTO, DATAHORA, SITUACAO FROM TBCOMENTARIO ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('IDPAI')
            collection.create_index('DATAHORA')
            collection.create_index([('ID', pymongo.ASCENDING), ('IDPAI', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])
            collection.create_index([('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])
            collection.create_index([('IDPAI', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('IDPAI', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])

        # rows = collection.find(filter={"ID": int(id_comentario)})
        # for row in rows:
        #     # logger.warning(f"  -> {row}")
        #     logger.warning(f"  -> {row['ID']} {row['IDUSUARIO']} {row['TEXTO'][:15]}"

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_comentario_reacao(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_comentario_reacao(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT IDCOMENTARIO, IDUSUARIO, TIPO FROM TBCOMENTARIO_REACAO ORDER BY IDCOMENTARIO, IDUSUARIO")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDCOMENTARIO')
            collection.create_index([('IDCOMENTARIO', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])
            collection.create_index([('IDCOMENTARIO', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING)])
            collection.create_index([('IDCOMENTARIO', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])

        # rows = db_mongo.db.usuarios_comentario_reacao.find(filter={"IDCOMENTARIO": int(id_comentario), "TIPO": 'A'})  # A-Gostei
        # rows = db_mongo.db.usuarios_comentario_reacao.find(filter={"IDCOMENTARIO": int(id_comentario), "TIPO": 'B'})  # B-NAO Gostei
        # rows = collection.aggregate(
        #     [
        #         {'$match': {"IDCOMENTARIO": int(id_comentario), "TIPO": 'A'}}, # A-Gostei
        #         {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIO', 'foreignField': 'ID', 'as': 'USER' }}, 
        #         {'$unwind': {'path': "$USER", 'preserveNullAndEmptyArrays': True }},
        #         {'$project': {'_id' : 0, 'IDCOMENTARIO' : 1, 'TIPO' : 1, 'IDUSUARIO' : 1, 'NOME' : "$USER.NOME", 'EMAIL' : "$USER.EMAIL" }},
        #     ]
        # )
        # rows = collection.aggregate(
        #     [
        #         {'$match': {"IDCOMENTARIO": int(id_comentario), "TIPO": 'B'}}, # B-NAO Gostei
        #         {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIO', 'foreignField': 'ID', 'as': 'USER' }}, 
        #         {'$unwind': {'path': "$USER", 'preserveNullAndEmptyArrays': True }},
        #         {'$project': {'_id' : 0, 'IDCOMENTARIO' : 1, 'TIPO' : 1, 'IDUSUARIO' : 1, 'NOME' : "$USER.NOME", 'EMAIL' : "$USER.EMAIL" }},
        #     ]
        # )
        # for row in rows:
        #     logger.warning(f"  -> {row['IDCOMENTARIO']} {row['IDUSUARIO']} {row['TIPO']} {row['NOME']} {row['EMAIL']}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_comentario_denuncia(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_comentario_denuncia(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT IDCOMENTARIO, IDUSUARIO, TIPO, SITUACAO FROM TBCOMENTARIO_DENUNCIA ORDER BY IDCOMENTARIO, IDUSUARIO")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDCOMENTARIO')
            collection.create_index('IDUSUARIO')
            collection.create_index([('IDCOMENTARIO', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_comentario_alerta(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_comentario_alerta(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDCOMENTARIO, IDUSUARIOORIG, IDUSUARIODSST, DTHR, TIPO, SITUACAO FROM TBCOMENTARIO_ALERTA ORDER BY ID, IDCOMENTARIO, IDUSUARIOORIG, IDUSUARIODSST")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDCOMENTARIO')
            collection.create_index([('IDUSUARIOORIG', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIODSST', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIOORIG', pymongo.ASCENDING), ('IDUSUARIODSST', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('IDCOMENTARIO', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('IDCOMENTARIO', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING), ('IDUSUARIODSST', pymongo.ASCENDING)])
            collection.create_index([('IDCOMENTARIO', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING), ('IDUSUARIOORIG', pymongo.ASCENDING)])

        # rows = collection.find(filter={"IDUSUARIODSST": int(id_usuario), "SITUACAO": 'P'}).sort("DTHR", -1).limit(5)  # P-Pendente
        # rows = db_mongo.db.usuarios_comentario_alerta.find(filter={"IDUSUARIODSST": int(id_usuario), "SITUACAO": 'P'}).sort("DTHR", -1).limit(5)  # P-Pendente
        # rows = db_mongo.db.usuarios_comentario_alerta.find(filter={"IDCOMENTARIO": int(id_comentario), "TIPO": {"$in": ['C','R'] }, "SITUACAO": 'L'})  # C-Comentário / R-Resposta  # L-Lido
        # rows = collection.aggregate(
        #     [
        #         {'$match': {'IDUSUARIODSST' : int(id_usuario), "SITUACAO": 'P'}},
        #         # {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIODSST', 'foreignField': 'ID', 'as': 'USERDSST' }}, 
        #         # {'$set': {"USERDSST": { '$arrayElemAt': ["$USERDSST", 0] } } },
        #         # {'$unwind': "$USERDSST" }, 
        #         # {'$unwind': {'path': "$USERDSST", 'preserveNullAndEmptyArrays': True }},
        #         {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIOORIG', 'foreignField': 'ID', 'as': 'USERORIG' }}, 
        #         # {'$set': {"USERORIG": { '$arrayElemAt': ["$USERORIG", 0] } } },
        #         # {'$unwind': "$USERORIG" },
        #         {'$unwind': {'path': "$USERORIG", 'preserveNullAndEmptyArrays': True }},
        #         # {'$project': {'_id' : 0, 'IDUSUARIOORIG' : 1, 'IDUSUARIODSST' : 1, 'SITUACAO' : 1, 'NOMEUSERORIG' : "$USERORIG.NOME", 'NOMEUSERDSST' : "$USERDSST.NOME" }},
        #         {'$project': {'_id' : 0, 'IDUSUARIOORIG' : 1, 'IDUSUARIODSST' : 1, 'SITUACAO' : 1, 'NMUSUARIOORIGEM' : "$USERORIG.NOME", 'FTUSUARIOORIGEM' : "$USERORIG.FOTO" }},
        #         {'$sort': {"DTHR": -1}},
        #         {'$limit': 3},
        #     ]
        # )
        # for row in rows:
        #     logger.warning(f"{row}")
            # logger.warning(f"{row['IDUSUARIOORIG']} {row['NOMEUSERORIG']} /\ {row['IDUSUARIODSST']} => {row['NOMEUSERDSST']}")

        # rows = collection.aggregate(
        #     [
        #         {'$match': {"IDCOMENTARIO": int(id_comentario), "TIPO": {"$in": ['C','R'] }, "SITUACAO": 'L'}},  # C-Comentário / R-Resposta  # L-Lido
        #         {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIODSST', 'foreignField': 'ID', 'as': 'USER' }}, 
        #         {'$unwind': {'path': "$USER", 'preserveNullAndEmptyArrays': True }},
        #         {'$project': {'_id' : 0, 'IDCOMENTARIO' : 1, 'TIPO' : 1, 'IDUSUARIODSST' : 1, 'SITUACAO' : 1, 'NOME' : "$USER.NOME", 'EMAIL' : "$USER.EMAIL" }},
        #     ]
        # )

        # for row in rows:
        #     logger.warning(f"  -> {row['IDCOMENTARIO']} {row['IDUSUARIODSST']} {row['NOME']} {row['EMAIL']}") 


    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_comentario_ajustar_id(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection_comentario = get_collection_usuarios_comentario(db=db)
        collection_reacao = get_collection_usuarios_comentario_reacao(db=db)
        collection_denuncia = get_collection_usuarios_comentario_denuncia(db=db)
        collection_alerta = get_collection_usuarios_comentario_alerta(db=db)

        # Primeira Parte
        # comets = collection_comentario.find({'ID': 817})  # .sort("ID", -1)  # .sort("DATAHORA", -1)
        # comets = collection_comentario.find({}) 

        # for coment in comets:
        #     try:

        #         id_comentario_novo   = ObjectId(coment['_id'])
        #         id_comentario_antigo = coment['ID']
        #         logger.warning(f"coment -> {id_comentario_novo} - {id_comentario_antigo}")

        #         collection_comentario.update_many({"IDPAI": id_comentario_antigo}, {"$set": {"IDPAI": id_comentario_novo}})
        #         # filhos = collection_comentario.find({'IDPAI': id_comentario_antigo})
        #         # for filho in filhos:
        #         #     # logger.warning(f"filho -> {filho['_id']} - {filho['ID']} - {filho['IDPAI']}")
        #         #     collection_comentario.update_one({"_id": filho["_id"]}, {"$set": {"IDPAI": id_comentario_novo}})

        #         collection_reacao.update_many({'IDCOMENTARIO': id_comentario_antigo}, {"$set": {"IDCOMENTARIO": id_comentario_novo}})
        #         # reacoes = collection_reacao.find({'IDCOMENTARIO': id_comentario_antigo})
        #         # for reacao in reacoes:
        #         #     # logger.warning(f"reacao -> {reacao['_id']} - {reacao['IDCOMENTARIO']}")
        #         #     collection_reacao.update_one({"_id": reacao["_id"]}, {"$set": {"IDCOMENTARIO": id_comentario_novo}})

        #         collection_denuncia.update_many({'IDCOMENTARIO': id_comentario_antigo}, {"$set": {"IDCOMENTARIO": id_comentario_novo}})
        #         # denuncias = collection_denuncia.find({'IDCOMENTARIO': id_comentario_antigo})
        #         # for denuncia in denuncias:
        #         #     # logger.warning(f"denuncia -> {denuncia['_id']} - {denuncia['IDCOMENTARIO']}")
        #         #     collection_denuncia.update_one({"_id": denuncia["_id"]}, {"$set": {"IDCOMENTARIO": id_comentario_novo}})

        #         collection_alerta.update_many({'IDCOMENTARIO': id_comentario_antigo}, {"$set": {"IDCOMENTARIO": id_comentario_novo}})
        #         # alertas = collection_alerta.find({'IDCOMENTARIO': id_comentario_antigo})
        #         # for alerta in alertas:
        #         #     # logger.warning(f"alerta -> {alerta['_id']} - {alerta['IDCOMENTARIO']}")
        #         #     collection_alerta.update_one({"_id": alerta["_id"]}, {"$set": {"IDCOMENTARIO": id_comentario_novo}})
        #         #     collection_alerta.update_one({"_id": alerta["_id"]}, {'$unset': {'ID': ""}})

        #     except Exception as e:
        #         logger.error(f'Falha Geral(main): "{str(e)}"')

        # Segunda Parte
        # collection_comentario.update_many({}, {'$unset': {'ID': ""}})
        # collection_alerta.update_many({}, {'$unset': {'ID': ""}})

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def  migrar_empresa_setor(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_setor(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, DESCRICAO, SITUACAO FROM TBEMPRESA_SETOR ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 


        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('DESCRICAO')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_subsetor(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_subsetor(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, DESCRICAO, SITUACAO FROM TBEMPRESA_SUBSETOR ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('DESCRICAO')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_segmento(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_segmento(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, DESCRICAO, SITUACAO FROM TBEMPRESA_SEGMENTO ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('DESCRICAO')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                query = """
                    SELECT E.ID, E.NOMRESUMIDO AS NOME, E.RAZAOSOCIAL, E.CNPJ, E.CODCVM, A.CODIGO, A.CODISIN, A.TIPO, E.SITUACAO, 'ACAO' AS CATEGORIA, A.VLRPRECOFECHAMENTO, A.VLRPRECOANTERIOR, A.VLRVARIACAO, A.DATAHORAALTERACO FROM TBEMPRESA E JOIN TBEMPRESA_ATIVO A ON (A.IDEMPRESA = E.ID)
                    UNION ALL
                    SELECT ID, NOME, RAZAOSOCIAL, CNPJ, '' AS CODCVM, CODIGO, CODISIN, '' AS TIPO, SITUACAO, 'FII' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBFII_FUNDOIMOB
                    UNION ALL
                    SELECT ID, FUNDO AS NOME, RAZAOSOCIAL, CNPJ, '' AS CODCVM, CODIGO, CODISIN, '' AS TIPO, SITUACAO, 'BETF' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBETF_INDICE
                    UNION ALL
                    SELECT ID, NOME, RAZAOSOCIAL, CNPJ, CODCVM, CODIGO, CODISIN, TIPO, SITUACAO, 'BDR' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBBDR_EMPRESA
                    UNION ALL
                    SELECT ID, NOME, NOME AS RAZAOSOCIAL, '00.000.000/0000-00' AS CNPJ, '' AS CODCVM, CODIGO, '' AS CODISIN, '' AS TIPO, SITUACAO, 'CRIPTO' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBCRIPTO_EMPRESA
                    ORDER BY CATEGORIA, CODIGO
                """
                cursor.execute(query)
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('NOME')
            collection.create_index('CODIGO')
            collection.create_index('CODISIN')
            collection.create_index([('ID', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('CODISIN', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_acao(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_acao(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT E.ID, E.IDSETOR, E.IDSUBSETOR, E.IDSEGMENTO, A.ID AS IDATIVO, E.NOME, E.NOMRESUMIDO, E.RAZAOSOCIAL, E.CNPJ, E.CODCVM, A.CODIGO, A.CODISIN, A.TIPO, E.SITUACAO, 'ACAO' AS CATEGORIA, A.VLRPRECOFECHAMENTO, A.VLRPRECOANTERIOR, A.VLRVARIACAO, A.DATAHORAALTERACO FROM TBEMPRESA E JOIN TBEMPRESA_ATIVO A ON (A.IDEMPRESA = E.ID) ORDER BY E.ID, A.ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('NOME')
            collection.create_index('NOMRESUMIDO')
            collection.create_index('CODIGO')
            collection.create_index('CODISIN')
            collection.create_index([('ID', pymongo.ASCENDING), ('CODISIN', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_fii(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_fii(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, IDFIITIPO, IDFIIADMIN, NOME, RAZAOSOCIAL, CNPJ, CODIGO, CODISIN, SITUACAO, 'FII' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBFII_FUNDOIMOB ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('NOME')
            collection.create_index('CODIGO')
            collection.create_index('CODISIN')
            collection.create_index([('ID', pymongo.ASCENDING), ('CODISIN', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_etf(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_etf(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, RAZAOSOCIAL, FUNDO, INDICE, NOME, CNPJ, CODIGO, CODISIN, SITUACAO, 'ETF' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBETF_INDICE ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('NOME')
            collection.create_index('CODIGO')
            collection.create_index('CODISIN')
            collection.create_index([('ID', pymongo.ASCENDING), ('CODISIN', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_bdr(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_bdr(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, IDSETOR, IDSUBSETOR, IDSEGMENTO, NOME, RAZAOSOCIAL, CNPJ, CODCVM, SITCVM, CODIGO, TIPO, CODISIN, SITUACAO, 'BDR' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBBDR_EMPRESA ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('NOME')
            collection.create_index('CODIGO')
            collection.create_index('CODISIN')
            collection.create_index([('ID', pymongo.ASCENDING), ('CODISIN', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('ID', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_cripto(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_cripto(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, NOME, CODIGO, SITUACAO, 'CRIPTO' AS CATEGORIA, VLRPRECOFECHAMENTO, VLRPRECOANTERIOR, VLRVARIACAO, DATAHORAALTERACO FROM TBCRIPTO_EMPRESA ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('ID')
            collection.create_index('NOME')
            collection.create_index('CODIGO')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, DENOM_CIA, CNPJ_CIA, ULT_ANO_REFER, ULT_TRI_REFER FROM TBEMPRESA_FINAN ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ULT_ANO_REFER', pymongo.ASCENDING)])
        
        # collection = db.teste
        # collection.delete_many({})

        # params = [
        #     {"CD_CVM": "100", "Nome": "Empresa 1", "ULT_ANO_REFER": "2020", "ULT_TRI_REFER": ""},
        #     {"CD_CVM": "200", "Nome": "Empresa 2", "ULT_ANO_REFER": "2021", "ULT_TRI_REFER": ""},
        #     {"CD_CVM": "300", "Nome": "Empresa 3", "ULT_ANO_REFER": "2022", "ULT_TRI_REFER": ""},
        #     {"CD_CVM": "400", "Nome": "Empresa 4", "ULT_ANO_REFER": "", "ULT_TRI_REFER": ""},
        # ]
        # collection.insert_many(params)

        # collection = db.teste_filho
        # collection.delete_many({})

        # params = [
        #     {"CD_CVM": "100", "ANO_REFER": "2020", 'TRI_REFER': '3'},
        #     {"CD_CVM": "200", "ANO_REFER": "2020", 'TRI_REFER': '3'},
        #     {"CD_CVM": "200", "ANO_REFER": "2021", 'TRI_REFER': '2'},
        #     {"CD_CVM": "300", "ANO_REFER": "2020", 'TRI_REFER': '3'},
        #     {"CD_CVM": "300", "ANO_REFER": "2021", 'TRI_REFER': '2'},
        #     {"CD_CVM": "300", "ANO_REFER": "2022", 'TRI_REFER': '1'},
        # ]
        # collection.insert_many(params)

        # collection = db.teste

        # rows = collection.aggregate(
        #     [
        #         {'$lookup': {'from': 'teste_filho', 'localField': 'CD_CVM', 'foreignField': 'CD_CVM', 'as': 'FILHO' }}, 
        #         {'$match': {'ULT_ANO_REFER': '', "FILHO": {'$exists': True, '$ne': []}}},
        #         {'$project': {'_id': 0, 'CD_CVM': 1, 'ANO_REFER': {'$max': "FILHO.ANO_REFER"}}},
        #     ]
        # )

        # params = []
        # for row in rows:
        #     if row['ANO_REFER']:
        #         params.append(UpdateOne({'CD_CVM': str(row['CD_CVM'])}, {'$set': {"ULT_ANO_REFER": str(row['ANO_REFER'])}}))
        # if len(params) > 0:
        #     collection.bulk_write(params, ordered=False)

        # rows = collection.find({})
        # for row in rows:
        #     logger.warning(f'{row}') 


    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_agenda(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_agenda(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, IDEMPRESA, NOME, CODIGO, DIVULGACAO, HORARIO FROM TBEMPRESA_FINAN_AGENDA ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDEMPRESA')
            collection.create_index('CODIGO')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_bpa_tri(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_bpa_tri(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, TRI_REFER, VLR_ATIVO_TOTAL, VLR_CIRCULANTE, VLR_CIRCULANTE_CAIXA, VLR_CIRCULANTE_APLIC_FINAN, VLR_CIRCULANTE_CONTAS_REC, VLR_CIRCULANTE_ESTOQUE, VLR_CIRCULANTE_OUTROS, VLR_NAO_CIRCULANTE, VLR_NAO_CIRCULANTE_LONGO_PRAZO, VLR_NAO_CIRCULANTE_INVESTIMENTOS, VLR_NAO_CIRCULANTE_IMOBILIZADO, VLR_NAO_CIRCULANTE_INTANGIVEL, VLR_NAO_CIRCULANTE_OUTROS FROM TBEMPRESA_FINAN_BPA_TRIMESTRAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING), ('TRI_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_bpa_ano(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_bpa_ano(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, VLR_ATIVO_TOTAL, VLR_CIRCULANTE, VLR_CIRCULANTE_CAIXA, VLR_CIRCULANTE_APLIC_FINAN, VLR_CIRCULANTE_CONTAS_REC, VLR_CIRCULANTE_ESTOQUE, VLR_CIRCULANTE_OUTROS, VLR_NAO_CIRCULANTE, VLR_NAO_CIRCULANTE_LONGO_PRAZO, VLR_NAO_CIRCULANTE_INVESTIMENTOS, VLR_NAO_CIRCULANTE_IMOBILIZADO, VLR_NAO_CIRCULANTE_INTANGIVEL, VLR_NAO_CIRCULANTE_OUTROS FROM TBEMPRESA_FINAN_BPA_ANUAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_bpp_tri(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_bpp_tri(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, TRI_REFER, VLR_PASSIVO_TOTAL, VLR_CIRCULANTE, VLR_CIRCULANTE_SALARIOS, VLR_CIRCULANTE_FORNECEDORES, VLR_CIRCULANTE_EMPRESTIMOSS, VLR_CIRCULANTE_OUTROS, VLR_NAO_CIRCULANTE, VLR_NAO_CIRCULANTE_EMPRESTIMOSS, VLR_NAO_CIRCULANTE_OUTROS, VLR_PATRIMONIO_LIQUIDO_CONSOLIDADO, VLR_PATRIMONIO_CAPITAL_SOCIAL_REALIZADO, VLR_PATRIMONIO_LUCRO_PREJUIZO_ACUMULADO, VLR_PATRIMONIO_RESERVA_CAPITAL, VLR_PATRIMONIO_RESERVA_LUCROS, VLR_PATRIMONIO_PARTICIPACAO_NAO_CONTROLADORES, VLR_PATRIMONIO_OUTROS FROM TBEMPRESA_FINAN_BPP_TRIMESTRAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING), ('TRI_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_bpp_ano(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_bpp_ano(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, VLR_PASSIVO_TOTAL, VLR_CIRCULANTE, VLR_CIRCULANTE_SALARIOS, VLR_CIRCULANTE_FORNECEDORES, VLR_CIRCULANTE_EMPRESTIMOSS, VLR_CIRCULANTE_OUTROS, VLR_NAO_CIRCULANTE, VLR_NAO_CIRCULANTE_EMPRESTIMOSS, VLR_NAO_CIRCULANTE_OUTROS, VLR_PATRIMONIO_LIQUIDO_CONSOLIDADO, VLR_PATRIMONIO_CAPITAL_SOCIAL_REALIZADO, VLR_PATRIMONIO_LUCRO_PREJUIZO_ACUMULADO, VLR_PATRIMONIO_RESERVA_CAPITAL, VLR_PATRIMONIO_RESERVA_LUCROS, VLR_PATRIMONIO_PARTICIPACAO_NAO_CONTROLADORES, VLR_PATRIMONIO_OUTROS FROM TBEMPRESA_FINAN_BPP_ANUAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_dfc_tri(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_dfc_tri(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, TRI_REFER, VLR_CAIXA_LIQUIDO_OPERAC, VLR_CAIXA_LIQUIDO_OPERAC_CAIXA_GERADO, VLR_CAIXA_LIQUIDO_OPERAC_VARIACOES, VLR_CAIXA_LIQUIDO_OPERAC_OUTROS, VLR_CAIXA_LIQUIDO_OPERAC_DEPRECIACAO_AMORTIZACAO, VLR_CAIXA_LIQUIDO_INVEST, VLR_CAIXA_LIQUIDO_FINAN, VLR_VARIACOES_CAMBIAL, VLR_CAIXA_EQUIVALENTE, VLR_CAIXA_EQUIVALENTE_SALDO_INICIA, VLR_CAIXA_EQUIVALENTE_SALDO_FINAL, VLR_CAIXA_TOTAL, VLR_CAIXA_LIVRE FROM TBEMPRESA_FINAN_DFC_TRIMESTRAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")
        
        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING), ('TRI_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_dfc_ano(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_dfc_ano(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, VLR_CAIXA_LIQUIDO_OPERAC, VLR_CAIXA_LIQUIDO_OPERAC_CAIXA_GERADO, VLR_CAIXA_LIQUIDO_OPERAC_VARIACOES, VLR_CAIXA_LIQUIDO_OPERAC_OUTROS, VLR_CAIXA_LIQUIDO_OPERAC_DEPRECIACAO_AMORTIZACAO, VLR_CAIXA_LIQUIDO_INVEST, VLR_CAIXA_LIQUIDO_FINAN, VLR_VARIACOES_CAMBIAL, VLR_CAIXA_EQUIVALENTE, VLR_CAIXA_EQUIVALENTE_SALDO_INICIA, VLR_CAIXA_EQUIVALENTE_SALDO_FINAL, VLR_CAIXA_TOTAL, VLR_CAIXA_LIVRE FROM TBEMPRESA_FINAN_DFC_ANUAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_dre_tri(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_dre_tri(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, TRI_REFER, VLR_RECEITA_LIQ, VLR_CUSTO, VLR_LUCRO_BRUTO, VLR_MARGEM_BRUTA, VLR_DESPESA_OPERAC, VLR_RESULTADO_OPERAC, VLR_MARGEM_OPERAC, VLR_RESULTADO_FINAN, VLR_RESULTADO_ANTES_IR, VLR_IMPOSTO, VLR_OPERAC_CONT, VLR_OPERAC_DESCONT, VLR_LUCRO_LIQUIDO, VLR_MARGEM_LIQUIDA FROM TBEMPRESA_FINAN_DRE_TRIMESTRAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING), ('TRI_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_finan_dre_ano(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_finan_dre_ano(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT ID, CD_CVM, ANO_REFER, VLR_RECEITA_LIQ, VLR_CUSTO, VLR_LUCRO_BRUTO, VLR_MARGEM_BRUTA, VLR_DESPESA_OPERAC, VLR_RESULTADO_OPERAC, VLR_MARGEM_OPERAC, VLR_RESULTADO_FINAN, VLR_RESULTADO_ANTES_IR, VLR_IMPOSTO, VLR_OPERAC_CONT, VLR_OPERAC_DESCONT, VLR_LUCRO_LIQUIDO, VLR_MARGEM_LIQUIDA FROM TBEMPRESA_FINAN_DRE_ANUAL ORDER BY ID ")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CD_CVM')
            collection.create_index([('CD_CVM', pymongo.ASCENDING), ('ANO_REFER', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    logger.info(f'Inicio') 
    try:

        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # load_dotenv(find_dotenv()) # os.getenv("CMS_DOMAIN")
        settings = Dynaconf(load_dotenv=True, environments=True, envvar_prefix="CMS_TNB")
        mysql_host, mysql_user, mysql_password, mysql_database, mongo_uri = settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASS, settings.MYSQL_DB, settings.MONGODB_URI
        logger.info(f'MONGODB = {mongo_uri}')
        logger.info(f'MYSQL   = {mysql_host} - {mysql_user} - {mysql_password} - {mysql_database}')

        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        # Ok DigitalOcean

        # migrar_noticia(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_admin_log_erros(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_config(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_log(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_apuracao(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_apuracao_calculada(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_comentario(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_comentario_reacao(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_comentario_denuncia(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_comentario_alerta(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_comentario_ajustar_id(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_agenda(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_bpa_tri(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_bpa_ano(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_bpp_tri(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_bpp_ano(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_dfc_tri(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_dfc_ano(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_dre_tri(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_finan_dre_ano(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)

        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        # Ok Localhost

        # migrar_empresa_setor(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_subsetor(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_segmento(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_acao(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_fii(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_etf(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_bdr(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_cripto(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)


        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        # Ok Desenv

        client     = get_client(mongo_uri=mongo_uri)
        db         = get_database(client=client)
        # collection = get_collection_usuarios(db=db)
        # collection = get_collection_usuarios_log(db=db)
        # collection = get_collection_usuarios_comentario(db=db)
        # collection = get_collection_usuarios_comentario_reacao(db=db)
        # collection = get_collection_usuarios_comentario_denuncia(db=db)
        # collection = get_collection_usuarios_comentario_alerta(db=db)
        # collection = get_collection_empresa_setor(db=db)
        # collection = get_collection_empresa_subsetor(db=db)
        # collection = get_collection_empresa_segmento(db=db)
        # collection = get_collection_empresa(db=db)
        # collection = get_collection_empresa_acao(db=db)
        # collection = get_collection_empresa_fii(db=db)
        # collection = get_collection_empresa_etf(db=db)
        # collection = get_collection_empresa_bdr(db=db)
        # collection = get_collection_empresa_cripto(db=db)

        # id_usuario = 2  # 2-CMS
        # tipo_usuario = 'A'   # I-Investidor  # A-Administrador
        # id_comentario = 784  # 784 # 796 # 800
        # #  uuid.uuid1()  # uuid.uuid4()  # uuid.uuid4().hex  # uuid.uuid4()  # UUID = uuid.uuid1()  UUID.int

        # Teste #1
        # Pesquisar nome   acao 'RAIZEN', fii 'FII HAZ', etf 'TREND OURO', bdr 'BKR US TREAS', cripto 'Polkadot' - na collection separadas
        # Pesquisar codigo acao 'MOSI3',  fii 'FLMA11',  etf 'XMAL11',     bdr 'S2TW34',       cripto 'SOL/BRL'  - na collection separadas

        # collection = get_collection_empresa_acao(db=db)
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'RAIZEN'})  # Done in 0.06s - 0:00:00.064183
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'MOSI3'}) #  Done in 0.00s - 0:00:00.002964
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # collection = get_collection_empresa_fii(db=db)
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'FII HAZ'})  # Done in 0.04s - 0:00:00.039146
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'FLMA11'}) #  Done in 0.00s - 0:00:00.003097
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # collection = get_collection_empresa_etf(db=db)
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'FUNDO': 'TREND OURO'})  # Done in 0.06s - 0:00:00.058358
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'XMAL11'}) #  Done in 0.01s - 0:00:00.007785
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # collection = get_collection_empresa_bdr(db=db)
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'BKR US TREAS'})  # Done in 0.06s - 0:00:00.063479
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'S2TW34'}) #  Done in 0.00s - 0:00:00.002934
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # collection = get_collection_empresa_cripto(db=db)
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'Polkadot'})  #  Done in 0.05s - 0:00:00.051656
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'SOL/BRL'}) #  Done in 0.00s - 0:00:00.002523
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # Teste #2
        # Pesquisar nome   acao 'RAIZEN', fii 'FII HAZ', etf 'TREND OURO', bdr 'BKR US TREAS', cripto 'Polkadot' - na mesma collection
        # Pesquisar codigo acao 'MOSI3',  fii 'FLMA11',  etf 'XMAL11',     bdr 'S2TW34',       cripto 'SOL/BRL'  - na mesma collection

        # collection = get_collection_empresa(db=db)

        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'RAIZEN'})  # Done in 0.05s - 0:00:00.045878
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'MOSI3'}) #  Done in 0.00s - 0:00:00.003023
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'FII HAZ'})  # Done in 0.05s - 0:00:00.051927
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'FLMA11'}) #  Done in 0.00s - 0:00:00.003667
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'TREND OURO'})  # Done in 0.07s - 0:00:00.070177
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'XMAL11'}) # Done in 0.01s - 0:00:00.005180
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'BKR US TREAS'})  # Done in 0.05s - 0:00:00.051732
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'S2TW34'}) # Done in 0.02s - 0:00:00.015949
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'NOME': 'Polkadot'})  # Done in 0.04s - 0:00:00.041101
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}') 
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CODIGO': 'SOL/BRL'}) # Done in 0.00s - 0:00:00.003383
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'{result["ID"]} - {result["CODIGO"]} - {result["NOME"]} - Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)}')

        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        collection = get_collection_usuarios(db=db)
        # collection = get_collection_usuarios_log(db=db)

        id_usuario = 2  # 2-CMS
        situaco = "A"  # A-Ativo
        # situaco = "L"  # L-xxxx
        # situaco = "P"  # P-Aguardando Confirmação de Email
        # situaco = "I"  # I-Inativo
        # dt_ini = "20220518" + "000000000"
        # dt_fim = ""  # "20220518" + "235959000"

        # rows = collection.find({'SITUACAO': situaco})
        # rows = collection.find({})

        rows = collection.aggregate(
            [
                {'$lookup': {'from': 'usuarios_log', 'localField': 'ID', 'foreignField': 'IDUSUARIO', 'pipeline': [{'$match': {'SITUACAO': 'L'}}], 'as': 'LOG_WEB'}},
                {'$lookup': {'from': 'usuarios_log', 'localField': 'ID', 'foreignField': 'IDUSUARIO', 'pipeline': [{'$match': {'SITUACAO': 'P'}}], 'as': 'LOG_APP'}}, 
                # {'$match': {'ID': id_usuario, 'SITUACAO': situaco}},
                {'$project': {'_id' : 0, 'ID' : 1, 'NOME' : 1, 'EMAIL' : 1, 'DTHR_WEB': {'$max': '$LOG_WEB.DATAHORA'}, 'DTHR_APP': {'$max': '$LOG_APP.DATAHORA'}}}, 
                # {'$sort': {"NOME": -1}},
            ]
        )

        lista = {row['ID']: {'DTHR_WEB': row['DTHR_WEB'] if row['DTHR_WEB'] else '', 'DTHR_APP': row['DTHR_APP'] if row['DTHR_APP'] else ''}  for row in rows if row['ID'] == 2 or row['ID'] == 7}

        # {k: v for v, k in enumerate(lst)}

        for row in lista:  # rows
            logger.warning(f'{row=}') 
            # logger.warning(f'{row["ID"]=} - {row["NOME"]=} - {row["EMAIL"]=} - {row["DTHR_WEB"]=} - {row["DTHR_APP"]=}') 

        logger.info(f'PESQUISA') 
        logger.warning(f'{lista=}') 
        # lista = {}
        # lista[2] = {'ID': 2, 'DTHR_WEB': '20220518204522275', 'DTHR_APP': '20220513104701045'}
        # lista[11] = {'ID': 2, 'DTHR_WEB': '20220518204522275', 'DTHR_APP': '20220513104701045'}
        logger.warning(f'{lista[2]["DTHR_WEB"]=}')
        logger.warning(f'{lista[2]["DTHR_WEB"]=}') 
        logger.warning(f'{lista.get(2)["DTHR_WEB"]=}') 
        logger.warning(f'{lista.get(7)["DTHR_WEB"]=}') 
        # logger.warning(f'{lista.get(10)["DTHR_WEB"]=}') 

        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


if __name__ == '__main__':
    main()

# python -m pip install --upgrade mysql-connector-python
# python -m pip install --upgrade PyMySQL
# python -m pip install --upgrade python-dotenv
# python -m pip install --upgrade dynaconf

# python main.py
