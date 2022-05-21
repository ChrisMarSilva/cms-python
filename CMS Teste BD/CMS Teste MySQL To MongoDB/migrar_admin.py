from loguru import logger
from pymongo import UpdateOne, UpdateMany
from bson.objectid import ObjectId
from mysql import get_connection_mysql
from mongo import *


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


def migrar_admin_fatos(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_admin_fatos(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT ID, DTFATO, IDFATOINI, IDFATOFIM, QTDPROC, DTHRREGISTRO, DTHRALTERACAO, SITUACAO FROM TBADMIN_FATOS ORDER BY ID")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('DTFATO')
            collection.create_index([('DTFATO', pymongo.ASCENDING), ('DTHRREGISTRO', pymongo.ASCENDING)])

        # collection = get_collection_admin_fatos(db=db)
        # rows = collection.find({'SITUACAO': {"$in": ['P', 'E']}, 'QTDPROC': {"$lt": 3}}).sort("DTFATO", -1)
        # lista = [{'ID': str(row['_id']), 'DTFATO': str(row['DTFATO']), 'IDFATOINI': int(row['IDFATOINI']), 'IDFATOFIM': int(row['IDFATOFIM'])} for row in rows]
        # logger.info(f'lista={len(lista)=}')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_admin_xxxxxxxx(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
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
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        # if lista:
        #     collection.create_index('xxxxxxxxx')
        #     collection.create_index([('xxxxxxxxx', pymongo.ASCENDING), ('xxxxxxxxx', pymongo.ASCENDING)])
        #     collection.create_index([('xxxxxxxxx', pymongo.ASCENDING), ('xxxxxxxxx', pymongo.ASCENDING), ('xxxxxxxxx', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
