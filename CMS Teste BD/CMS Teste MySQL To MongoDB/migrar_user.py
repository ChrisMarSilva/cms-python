from loguru import logger
from math import ceil  # floor
from pymongo import UpdateOne, UpdateMany
from bson.objectid import ObjectId
from mysql import get_connection_mysql
from mongo import *


def migrar_usuario(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, NOME, EMAIL, SENHA, DTREGISTRO, TENTATIVA, TIPO, SITUACAO, FOTO, CHATID, HASH FROM TBUSUARIO ORDER BY ID")
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
        
        # rows = collection.aggregate(
        #     [
        #         {'$lookup': {'from': 'usuarios_log', 'localField': 'ID', 'foreignField': 'IDUSUARIO', 'pipeline': [{'$match': {'SITUACAO': 'L'}}], 'as': 'LOG_WEB'}},
        #         {'$lookup': {'from': 'usuarios_log', 'localField': 'ID', 'foreignField': 'IDUSUARIO', 'pipeline': [{'$match': {'SITUACAO': 'P'}}], 'as': 'LOG_APP'}}, 
        #         # {'$match': {'ID': id_usuario, 'SITUACAO': situaco}},
        #         {'$project': {'_id' : 0, 'ID' : 1, 'NOME' : 1, 'EMAIL' : 1, 'DTHR_WEB': {'$max': '$LOG_WEB.DATAHORA'}, 'DTHR_APP': {'$max': '$LOG_APP.DATAHORA'}}}, 
        #         # {'$sort': {"NOME": -1}},
        #     ]
        # )

        # lista = {row['ID']: {'DTHR_WEB': row['DTHR_WEB'] if row['DTHR_WEB'] else '', 'DTHR_APP': row['DTHR_APP'] if row['DTHR_APP'] else ''}  for row in rows if row['ID'] == 2 or row['ID'] == 7}

        # for row in lista:  # rows
        #     logger.warning(f'{row=}') 
            # logger.warning(f'{row["ID"]=} - {row["NOME"]=} - {row["EMAIL"]=} - {row["DTHR_WEB"]=} - {row["DTHR_APP"]=}') 

        # logger.warning(f'{lista[2]["DTHR_WEB"]=}')
        # logger.warning(f'{lista.get(2)["DTHR_WEB"]=}') 

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
        #         logger.error(f'Falha Geral: "{str(e)}"')

        # Segunda Parte
        # collection_comentario.update_many({}, {'$unset': {'ID': ""}})
        # collection_alerta.update_many({}, {'$unset': {'ID': ""}})

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_nota_corretagem(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_nota_corretagem(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDUSUARIO, IDCORRETORA, NMARQUIVO, PATHARQUIVO, DTIMPORTACAO, DTHRREGISTRO, DTHRALTERACAO, SITUACAO FROM TBNOTA_CORRETAGEM ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DTIMPORTACAO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DTIMPORTACAO', pymongo.ASCENDING), ('IDCORRETORA', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('NMARQUIVO', pymongo.ASCENDING)])
            collection.create_index('SITUACAO')
            collection.create_index([('_id', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])


        # collection_nota_corretagem      = get_collection_usuarios_nota_corretagem(db=db)
        # collection_nota_corretagem_data = get_collection_usuarios_nota_corretagem_data(db=db)
        # collection_nota_corretagem_oper = get_collection_usuarios_nota_corretagem_oper(db=db)

        # id_usuario = 2  # 2-CMS
        # id_corretora = 3  # 3-MODAL
        # dt_ini     = '20220313'
        # dt_fim     = '20220314'

        # filters = {'IDUSUARIO': id_usuario, 'DTIMPORTACAO': {'$gte': dt_ini, '$lte': dt_fim}}
        # filters['IDCORRETORA'] = id_corretora
        # logger.warning(f"{filters=}")

        # rows = collection_nota_corretagem.find(filters).sort([["DTIMPORTACAO", -1], ["_id", -1]])

        # rows = collection_nota_corretagem.aggregate(
        #     [
        #         {'$lookup': {'from': 'usuarios_nota_corretagem_oper', 'localField': '_id', 'foreignField': 'IDNOTACORRETAGEM', 'as': 'OPER' }}, 
        #         #{'$match': {'_id': ObjectId('6286cc3faccb811332432e30')}},
        #         {'$match': filters},
        #         {'$project': {'_id' : 1, 'IDUSUARIO' : 1, 'IDCORRETORA' : 1, 'NMARQUIVO' : 1, 'DTIMPORTACAO' : 1, 'DTHRREGISTRO' : 1, 'DTHRALTERACAO' : 1, 'SITUACAO' : 1, 'OPER': '$OPER.SITUACAO'}}, 
        #         {'$sort': {"DTIMPORTACAO": -1, "_id": -1}},
        #     ]
        # )

        # logger.warning(f"{rows.count()=}")

        # for row in rows:
        #     logger.warning(f"{row}")
            # QTDE_OPER_IMPORT = len(row['OPER'])
            # QTDE_OPER_PEND = len([item for item in row['OPER'] if str(item) == 'P'])
            # QTDE_OPER_ADD = len([item for item in row['OPER'] if str(item) == 'A'])
            # QTDE_OPER_CONF = len([item for item in row['OPER'] if str(item) == 'F'])
            # logger.warning(f"{row['_id']} - {row['NMARQUIVO']} - {row['DTHRREGISTRO']} - {row['DTHRALTERACAO']} - {row['SITUACAO']} - {QTDE_OPER_IMPORT=} - {QTDE_OPER_PEND=} - {QTDE_OPER_ADD=} - {QTDE_OPER_CONF=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_nota_corretagem_data(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_nota_corretagem_data(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDNOTACORRETAGEM, DTNOTA, QTDOPER, VLRLIQUIDOOPERACAO, VLRTXLIQUIDACAO, VLRTXEMOLUMENTOS, VLRTXCORRETAGEM, VLRTXISS, VLRTXIRRF, VLRTXOUTRAS, VLRTXTOTAL, VLRLIQUIDOTOTAL, DTHRREGISTRO, DTHRALTERACAO, SITUACAO FROM TBNOTA_CORRETAGEM_DATA ORDER BY ID")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDNOTACORRETAGEM')
            collection.create_index([('IDNOTACORRETAGEM', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_nota_corretagem_oper(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_nota_corretagem_oper(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDNOTACORRETAGEM, IDATIVO, TPATIVO, CODIGO, DATA, TIPO, QUANT, VLRPRECO, VLRPRECOTOTAL, VLRTXLIQUIDACAO, VLRTXEMOLUMENTOS, VLRTXCORRETAGEM, VLRTXISS, VLRTXIRRF, VLRTXOUTRAS, VLRTXTOTAL, VLRTOTAL, DTHRREGISTRO, DTHRALTERACAO, SITUACAO FROM TBNOTA_CORRETAGEM_OPER ORDER BY ID")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDNOTACORRETAGEM')
            collection.create_index([('IDNOTACORRETAGEM', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_nota_corretagem_ajustar_id(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db     = get_database(client=client)

        collection_nota_corretagem      = get_collection_usuarios_nota_corretagem(db=db)
        collection_nota_corretagem_data = get_collection_usuarios_nota_corretagem_data(db=db)
        collection_nota_corretagem_oper = get_collection_usuarios_nota_corretagem_oper(db=db)

        notas = collection_nota_corretagem.find({}) 

        for nota in notas:
            try:

                id_nota_novo   = ObjectId(nota['_id'])
                id_nota_antigo = nota['ID']
                # logger.warning(f"notas -> {id_nota_novo} - {id_nota_antigo}")

                collection_nota_corretagem_data.update_many({'IDNOTACORRETAGEM': id_nota_antigo}, {"$set": {"IDNOTACORRETAGEM": id_nota_novo}})
                collection_nota_corretagem_oper.update_many({'IDNOTACORRETAGEM': id_nota_antigo}, {"$set": {"IDNOTACORRETAGEM": id_nota_novo}})

            except Exception as e:
                logger.error(f'Falha Geral: "{str(e)}"')

        collection_nota_corretagem.update_many({}, {'$unset': {'ID': ""}})
        collection_nota_corretagem_data.update_many({}, {'$unset': {'ID': ""}})
        collection_nota_corretagem_oper.update_many({}, {'$unset': {'ID': ""}})

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_carteira_projecao(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_carteira_projecao(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDUSUARIO, DESCRICAO, SITUACAO FROM TBCARTEIRA_PROJECAO ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDUSUARIO')
            collection.create_index([('_id', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DESCRICAO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

        # collection_carteira_projecao      = get_collection_usuarios_carteira_projecao(db=db)
        # collection_carteira_projecao_item = get_collection_usuarios_carteira_projecao_item(db=db)

        # rows = collection_carteira_projecao_item.aggregate(
        #     [
        #         {'$lookup': {'from': 'usuarios_carteira_projecao', 'localField': 'IDPROJECAO', 'foreignField': '_id', 'as': 'PROJ' }}, 
        #         {'$match': {"IDPROJECAO": ObjectId('6288edcc6415bdf493250515'), 'PROJ.IDUSUARIO': 2}},
        #         {'$project': {'_id' : 0, 'NUMERO' : 1, 'ANO' : 1, 'MES' : 1, 'VLRINVESTINI' : 1, 'VLRINVESTMES' : 1, 'VLRINVESTFIM' : 1, 'RENDMENSAL' : 1, 'TIPO' : 1}},
        #         {'$sort': {"NUMERO": -1}},
        #     ]
        # )

        # for row in rows:
        #     logger.warning(f"{row}")
        #     # logger.warning(f"{row['NUMERO']} - {row['ANO']} - {row['MES']} - {row['VLRINVESTINI']} - {row['VLRINVESTMES']} - {row['VLRINVESTFIM']} - {row['RENDMENSAL']}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_carteira_projecao_item(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_carteira_projecao_item(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT IDPROJECAO, NUMERO, ANO, MES, VLRINVESTINI, VLRINVESTMES, VLRINVESTFIM, RENDMENSAL, TIPO, SITUACAO FROM TBCARTEIRA_PROJECAO_ITEM ORDER BY IDPROJECAO, NUMERO, ANO, MES")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDPROJECAO')
            collection.create_index([('IDPROJECAO', pymongo.ASCENDING), ('NUMERO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_carteira_projecao_ajustar_id(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db     = get_database(client=client)

        collection_projecao      = get_collection_usuarios_carteira_projecao(db=db)
        collection_projecao_item = get_collection_usuarios_carteira_projecao_item(db=db)

        notas = collection_projecao.find({}) 

        for nota in notas:
            try:

                id_projecao_novo   = ObjectId(nota['_id'])
                id_projecao_antigo = nota['ID']
                # logger.warning(f"notas -> {id_projecao_novo} - {id_projecao_antigo}")

                collection_projecao_item.update_many({'IDPROJECAO': id_projecao_antigo}, {"$set": {"IDPROJECAO": id_projecao_novo}})

            except Exception as e:
                logger.error(f'Falha Geral: "{str(e)}"')

        collection_projecao.update_many({}, {'$unset': {'ID': ""}})
        collection_projecao_item.update_many({}, {'$unset': {'ID': ""}})

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_cei(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_cei(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, IDUSUARIO, CPF, SENHA, DTHRREGISTRO, DTHRALTERACAO, TIPO, SITUACAO FROM TBCEI ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDUSUARIO')

        # collection_cei      = get_collection_usuarios_cei(db=db)
        # collection_cei_oper = get_collection_usuarios_cei_oper(db=db)
        # collection_cei_prov = get_collection_usuarios_cei_prov(db=db)

        # rows = collection_cei_oper.find({'IDUSUARIO': 2}).sort("CODIGO", 1).distinct('CODIGO')
        # rows = collection_cei_oper.distinct('CODIGO', {'IDUSUARIO': 2})
        # lista = [[str(row['CODIGO']), str(row['CODIGO']), str(row['CODIGO'])] for row in rows]

        # for row in rows:
        #     logger.warning(f"{row}")
            # logger.warning(f"{row['CODIGO']}")

        # lista = [[str(row), str(row), str(row)] for row in rows]
        # logger.warning(f"{lista}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_cei_oper(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_cei_oper(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBCEI_OPER%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas = {len(tabelas)}") 

                lista = []
                for tabela in tabelas:
                    # logger.info(f"{tabela['TABLE_NAME']=}") 
                    cursor.execute(f"SELECT ID, IDUSUARIO, CATEGORIA, DATA, TIPO, CODIGO, QUANT, PRECO, TOTAL, CORRET_ID, CORRET_NOME, CORRET_CONTA, SITUACAO FROM {tabela['TABLE_NAME']} ORDER BY ID")
                    result = cursor.fetchall()
                    lista += [convert_decimal(row) for row in result]  # lista = [row for row in result]

        logger.info(f"Total MySQL = {len(lista)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('IDUSUARIO')
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])
            collection.create_index([('_id', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])
            collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_cei_prov(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_cei_prov(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBCEI_PROV%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas = {len(tabelas)}") 

                lista = []
                for tabela in tabelas:
                    # logger.info(f"{tabela['TABLE_NAME']=}") 
                    cursor.execute(f"SELECT ID, IDUSUARIO, CATEGORIA, CODIGO, DATA_PAGTO, TIPO, QUANT, TOTAL_BRUTO, TOTAL_LIQUIDO, CORRET_ID, CORRET_NOME, CORRET_CONTA, SITUACAO FROM {tabela['TABLE_NAME']} ORDER BY ID")
                    result = cursor.fetchall()
                    lista += [convert_decimal(row) for row in result]  # lista = [row for row in result]

        logger.info(f"Total MySQL = {len(lista)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        # if lista:
        collection.create_index('IDUSUARIO')
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])
        collection.create_index([('_id', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_cei_ajustar_id(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db     = get_database(client=client)

        collection_cei      = get_collection_usuarios_cei(db=db)
        collection_cei_oper = get_collection_usuarios_cei_oper(db=db)
        collection_cei_prov = get_collection_usuarios_cei_prov(db=db)

        collection_cei.update_many({}, {'$unset': {'ID': ""}})
        collection_cei_oper.update_many({}, {'$unset': {'ID': ""}})
        collection_cei_prov.update_many({}, {'$unset': {'ID': ""}})

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_empresa_fatos(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db     = get_database(client=client)

        collection = get_collection_usuarios_empresa_fatos(db=db)

        collection.create_index('IDUSUARIO')
        collection.create_index([('_id', pymongo.ASCENDING), ('IDUSUARIO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('IDFATO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('PROTOCOLO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('DATA_REF', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('DATA_ENV', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('IDEMPRESA', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('IDEMPRESA', pymongo.ASCENDING), ('DATA_ENV', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('ORIGEM', pymongo.ASCENDING), ('DATA_ENV', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

        # collection_empresa = get_collection_empresa(db=db)
        # rows = collection_empresa.find({'CATEGORIA': {'$in': ['ACAO', 'FII', 'ETF', 'BDR', 'CRIPTO']}, 'SITUACAOATIVO': {'$in': ['A', 'E']}})
        # rows = collection_empresa.find({'SITUACAOATIVO': {'$in': ['A', 'E']}}).sort('CODIGO', 1)
        # rows = collection_empresa.find({'CATEGORIA': {'$in': ['ETF']}, 'SITUACAOATIVO': {'$in': ['A', 'E']}})
        # total = rows.count()
        # logger.warning(f'{total=}')
        # for idx, row in enumerate(rows):
        #     # if idx == 0 or idx == total - 1: 
        #     # logger.warning(f'{idx+1}/{total} - {row}')
        #     logger.warning(f'{idx+1}/{total} - {row["CATEGORIA"]} - {row["CODIGO"]} - {row["IDATIVO"]} - {row["NOMERESUMIDO"]}')

        # collection_empresa_fatos = get_collection_empresa_fatos(db=db)
        # result = collection_empresa_fatos.count_documents({"CATEGORIA": 'ACAO'}).explain() # executionStats
        # result = collection_empresa_fatos.find({'CATEGORIA': 'ACAO'}).skip(1).limit(100).sort('DATA_ENV', -1)  # .explain("executionStats") # .explain()
        # logger.warning(f'{result=}')  
        # for row in result:
        #     logger.warning(f'{row=}')
        #     break

        # collection = db.teste
        # collection.delete_many({})
        # lista = [
        #     {'ID': 1, 'VLRPRECOFECHAMENTO': Decimal128(str(float(10.0))), 'VLRPRECOANTERIOR': Decimal128(str(float(15.0))), 'VLRVARIACAO': Decimal128(str(float(1.5)))},
        #     {'ID': 2, 'VLRPRECOFECHAMENTO': Decimal128(str(float(20.0))), 'VLRPRECOANTERIOR': Decimal128(str(float(25.0))), 'VLRVARIACAO': Decimal128(str(float(2.5)))},
        # ]
        # collection.insert_many(lista)
        # # collection.update_many({}, {'$set': {'VLRPRECOANTERIOR': '$VLRPRECOFECHAMENTO', 'VLRVARIACAO': Decimal128(str(float(0.0)))}})
        # # collection.update_many({},[{'$set': {"VLRPRECOANTERIOR": "$VLRPRECOFECHAMENTO", 'VLRVARIACAO': Decimal128(str(float(0.0)))}}], {'multi': 'true'})
        # collection.update_many({}, [{'$set': {"VLRPRECOANTERIOR": "$VLRPRECOFECHAMENTO", 'VLRVARIACAO': Decimal128(str(float(0.0))), "DATAHORAALTERACO": ""}}])
        # result = collection.find({})
        # for row in result:
        #     logger.warning(f'{row=}')


        # collection_empresa               = get_collection_empresa(db=db)
        # collection_usuario               = get_collection_usuarios(db=db)
        # collection_usuario_empresa_fatos = get_collection_usuarios_empresa_fatos(db=db)
        # collection_empresa_fatos         = get_collection_empresa_fatos(db=db)

        # # if collection_usuario_empresa_fatos.count_documents({}) <= 0: logger.warning(f'DELETANDO TUDO')
        # collection_usuario_empresa_fatos.delete_many({})
        # # lista = [ {'IDUSUARIO': 1, 'CATEGORIA': 'ACAO', 'IDFATO': 10, 'DATA_REF': '20220501', 'PROTOCOLO': 100}, {'IDUSUARIO': 2, 'CATEGORIA': 'ACAO', 'IDFATO': 20, 'DATA_REF': '20220502', 'PROTOCOLO': 200}, ]
        # # collection_usuario_empresa_fatos.insert_many(lista)

        # listar usuario com ativos na carteira ou no radar
        # users = collection_usuario.find({'ID': 2}).sort('ID', 1)
        # total = users.count()
        # data_ini_mes = '20220501'
        # logger.warning(f'{data_ini_mes=}')
        # for idx, user in enumerate(users):
        #     id_usuario = int(user["ID"])
        #     logger.warning(f'{idx+1}/{total} - {user["_id"]} - {user["ID"]} - {user["NOME"]} - {user["EMAIL"]}')
        #     #    buscar lista de ativos da carteira ou do radar
        #     companies = collection_empresa.find({'CATEGORIA': 'ACAO', 'CODIGO': {'$in': ['ITSA4', 'FESA4', 'GFSA3']}})
        #     empresas = [int(empresa['IDEMPRESA']) for empresa in companies if empresa['IDEMPRESA']]
        #     logger.warning(f'{empresas=}')
        #     #    buscar o maior protocolo do usuario
        #     user_fato = collection_usuario_empresa_fatos.find_one(filter={'IDUSUARIO': id_usuario}, sort=[("PROTOCOLO", -1)], limit=1)  # max
        #     protocolo = int(user_fato['PROTOCOLO']) if user_fato else 0
        #     logger.warning(f'{protocolo=}')
        #     #    buscar todos os fatos relevantes do mes, para aqueles ativos, maior que o max protocolo usuario
        #     facts = collection_empresa_fatos.find({'CATEGORIA': 'ACAO', 'IDEMPRESA': {'$in': empresas}, 'DATA_REF': {'$gte': data_ini_mes}, 'PROTOCOLO': {'$gt': protocolo}, 'SITUACAO': 'A'})
        #     fatos = [{'IDUSUARIO': id_usuario, 'CATEGORIA': fato['CATEGORIA'], 'ORIGEM': fato['CATEGORIA'], 'IDFATO': fato['_id'], 'IDEMPRESA': int(fato['IDEMPRESA']), 'NMEMPRESA': fato['NMEMPRESA'], 'DATA_ENV': fato['DATA_ENV'], 'DATA_REF': fato['DATA_REF'], 'PROTOCOLO': int(fato['PROTOCOLO']), 'LINK': fato['LINK'], 'ASSUNTO': fato['ASSUNTO'], 'SITUACAO': 'P'}  for fato in facts] #P-Pendente
        #     logger.warning(f'{fatos=}')
        #     logger.warning(f'{len(fatos)=}')
        #     if fatos: collection_usuario_empresa_fatos.insert_many(fatos)

        # RESETAR DADOS USUARIO
        # user_fato = collection_usuario_empresa_fatos.find_one(filter={'IDUSUARIO': 2}, sort=[("PROTOCOLO", -1)], limit=1)  # max
        # protocolo = int(user_fato['PROTOCOLO']) if user_fato else 0
        # logger.warning(f'{protocolo=}')
        # collection_usuario_empresa_fatos.delete_many({"IDUSUARIO": 2, 'PROTOCOLO': {'$lt': protocolo}})  # $lt <
        # collection_usuario_empresa_fatos.update_many({"IDUSUARIO": 2}, {"$set": {"SITUACAO": 'L'}})  # L-Lido

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_empresa_proventos(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_usuarios_empresa_proventos(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                query = """
                    SELECT T.CATEGORIA, T.IDUSUARIO, T.IDATIVO, T.IDPROVENTO
                    FROM ( 
                        SELECT 'ACAO' AS CATEGORIA, PA.IDUSUARIO, PA.IDATIVO AS IDATIVO, PA.IDEMPRPROV AS IDPROVENTO FROM TBEMPRESA_PROVENTO_ATIVO PA
                        UNION ALL
                        SELECT 'FII'  AS CATEGORIA, PA.IDUSUARIO, PA.IDFUNDO AS IDATIVO, PA.IDEMPRPROV AS IDPROVENTO FROM TBFII_FUNDOIMOB_PROVENTO_ATIVO PA
                        UNION ALL
                        SELECT 'BDR'  AS CATEGORIA, PA.IDUSUARIO, PA.IDBDR   AS IDATIVO, PA.IDBDRPROV  AS IDPROVENTO FROM TBBDR_EMPRESA_PROVENTO_ATIVO PA
                    )T
                    ORDER BY T.IDUSUARIO, T.CATEGORIA, T.IDATIVO, T.IDPROVENTO
                """
                cursor.execute(query)
                result = cursor.fetchall()
                rows = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        collection_empresa_proventos = get_collection_empresa_proventos(db=db)

        lista = []
        for row in rows:
            prov = collection_empresa_proventos.find_one({'CATEGORIA': row['CATEGORIA'], 'IDPROVENTO': row['IDPROVENTO']})
            if not prov: 
                logger.error(f"NÃO LOCALIZADO - {row['CATEGORIA']=} - {row['IDPROVENTO']=}")
                continue
            lista.append({'IDUSUARIO': int(row['IDUSUARIO']), "CATEGORIA": prov['CATEGORIA'], "IDATIVO": prov['IDATIVO'], "CODIGO": prov['CODIGO'], "IDPROVENTO": prov['_id'], "IDEMPRESA": prov['IDEMPRESA'], "NMEMPRESA": prov['NMEMPRESA'], "TIPO": prov['TIPO'], "CATEG": prov['CATEG'], "CODISIN": prov['CODISIN'], "DATAAPROV": prov['DATAAPROV'], "DATACOM": prov['DATACOM'], "DATAEX": prov['DATAEX'], "DATAPAGTO": prov['DATAPAGTO'], "VLRPRECO": prov['VLRPRECO'], "SITUACAO": 'L'})  # L-Lido
            # break

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        # if lista:
        collection.create_index('IDUSUARIO')
        collection.create_index('CATEGORIA')
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('IDPROVENTO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('IDATIVO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('DATAEX', pymongo.ASCENDING), ('DATAPAGTO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
        collection.create_index([('IDUSUARIO', pymongo.ASCENDING), ('CATEGORIA', pymongo.ASCENDING), ('DATAEX', pymongo.ASCENDING), ('DATAPAGTO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_usuario_xxxxxxxx(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_xxxxxxxx(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT xxxxxxx FROM xxxxxxxx ORDER BY xxxxxxxxx")
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        # if lista:
        #     collection.create_index('xxxxxxxxx')
        #     collection.create_index([('xxxxxxxxx', pymongo.ASCENDING), ('xxxxxxxxx', pymongo.ASCENDING)])
        #     collection.create_index([('xxxxxxxxx', pymongo.ASCENDING), ('xxxxxxxxx', pymongo.ASCENDING), ('xxxxxxxxx', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
