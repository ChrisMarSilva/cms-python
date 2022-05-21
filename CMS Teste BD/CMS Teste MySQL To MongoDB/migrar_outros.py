from loguru import logger
from pymongo import UpdateOne, UpdateMany
from bson.objectid import ObjectId
from mysql import get_connection_mysql
from mongo import *



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


def migrar_xxxxxxxx(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
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
