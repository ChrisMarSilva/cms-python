from loguru import logger
from pymongo import UpdateOne, UpdateMany
from bson.objectid import ObjectId
from mysql import get_connection_mysql
from mongo import *


def  migrar_empresa_admin(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_admin(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT 'FII' CATEGORIA, ID, NOME, CNPJ, SITUACAO FROM TBFII_FUNDOIMOB_ADMIN ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CATEGORIA')
            collection.create_index('NOME')
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('ID', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('NOME', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def  migrar_empresa_setores(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_setores(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(" SELECT 'ACAO' CATEGORIA, 'SETOR' AS TIPO, ID, DESCRICAO, SITUACAO FROM TBEMPRESA_SETOR ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL - ACAO - SETOR = {len(lista)}") 
                if lista: collection.insert_many(lista)

                cursor.execute(" SELECT 'ACAO' CATEGORIA, 'SUBSETOR' AS TIPO, ID, DESCRICAO, SITUACAO FROM TBEMPRESA_SUBSETOR ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL - ACAO - SUBSETOR = {len(lista)}") 
                if lista: collection.insert_many(lista)

                cursor.execute(" SELECT 'ACAO' CATEGORIA, 'SEGMENTO' AS TIPO, ID, DESCRICAO, SITUACAO FROM TBEMPRESA_SEGMENTO ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL - ACAO - SEGMENTO = {len(lista)}") 
                if lista: collection.insert_many(lista)

                cursor.execute(" SELECT 'FII' CATEGORIA, 'TIPO' AS TIPO, ID, DESCRICAO, SITUACAO FROM TBFII_FUNDOIMOB_TIPO ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL - FII - TIPO = {len(lista)}") 
                if lista: collection.insert_many(lista)

                cursor.execute(" SELECT 'BDR' CATEGORIA, 'SETOR' AS TIPO, ID, DESCRICAO, SITUACAO FROM TBBDR_EMPRESA_SETOR ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL - BDR - SETOR = {len(lista)}") 
                if lista: collection.insert_many(lista)

                cursor.execute(" SELECT 'BDR' CATEGORIA, 'SUBSETOR' AS TIPO, ID, DESCRICAO, SITUACAO FROM TBBDR_EMPRESA_SUBSETOR ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL - BDR - SUBSETOR = {len(lista)}") 
                if lista: collection.insert_many(lista)

                cursor.execute(" SELECT 'BDR' CATEGORIA, 'SEGMENTO' AS TIPO, ID, DESCRICAO, SITUACAO FROM TBBDR_EMPRESA_SEGMENTO ORDER BY ID ")
                result = cursor.fetchall()
                lista = [row for row in result]
                logger.info(f"Total MySQL - BDR - SEGMENTO = {len(lista)}") 
                if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CATEGORIA')
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('ID', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('DESCRICAO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('TIPO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING), ('DESCRICAO', pymongo.ASCENDING)])

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
                    SELECT 'ACAO'   CATEGORIA, A.ID AS IDATIVO, A.CODIGO,     A.TIPO,     A.CODISIN, A.VLRPRECOFECHAMENTO, A.VLRPRECOANTERIOR, A.VLRVARIACAO, A.DATAHORAALTERACO, A.SITUACAO AS SITUACAOATIVO, E.ID AS IDEMPRESA, E.NOME, E.NOMRESUMIDO AS NOMERESUMIDO,         E.RAZAOSOCIAL,                      E.CNPJ,      E.CODCVM,     E.SITE,           E.TIPO_MERCADO,       E.IDSETOR, IFNULL(ST.DESCRICAO, 'Não Classificados') AS NMSETOR,       E.IDSUBSETOR, IFNULL(SB.DESCRICAO, 'Não Classificados') AS NMSUBSETOR,       E.IDSEGMENTO, IFNULL(SG.DESCRICAO, 'Não Classificados') AS NMSEGMENTO, E.SITUACAO AS SITUACAOEMPRESA FROM TBEMPRESA E JOIN TBEMPRESA_ATIVO A ON (A.IDEMPRESA = E.ID) LEFT JOIN TBEMPRESA_SETOR ST ON (ST.ID = E.IDSETOR) LEFT JOIN TBEMPRESA_SUBSETOR SB ON (SB.ID = E.IDSUBSETOR) LEFT JOIN TBEMPRESA_SEGMENTO SG ON (SG.ID = E.IDSEGMENTO)
                    UNION ALL
                    SELECT 'FII'    CATEGORIA, E.ID AS IDATIVO, E.CODIGO, '' AS TIPO,     E.CODISIN, E.VLRPRECOFECHAMENTO, E.VLRPRECOANTERIOR, E.VLRVARIACAO, E.DATAHORAALTERACO, E.SITUACAO AS SITUACAOATIVO, E.ID AS IDEMPRESA, E.NOME,        E.NOME AS NOMERESUMIDO,         E.RAZAOSOCIAL,                       E.CNPJ, '' AS CODCVM, '' AS SITE,    'FII' AS TIPO_MERCADO, NULL AS IDSETOR,        'FII' AS NMSETOR, NULL AS IDSUBSETOR,        'FII' AS NMSUBSETOR, NULL AS IDSEGMENTO,        'FII' AS NMSEGMENTO, E.SITUACAO AS SITUACAOEMPRESA FROM TBFII_FUNDOIMOB E
                    UNION ALL
                    SELECT 'ETF'    CATEGORIA, E.ID AS IDATIVO, E.CODIGO, '' AS TIPO,     E.CODISIN, E.VLRPRECOFECHAMENTO, E.VLRPRECOANTERIOR, E.VLRVARIACAO, E.DATAHORAALTERACO, E.SITUACAO AS SITUACAOATIVO, E.ID AS IDEMPRESA, E.NOME,       E.FUNDO AS NOMERESUMIDO,         E.RAZAOSOCIAL,                       E.CNPJ, '' AS CODCVM, '' AS SITE,    'ETF' AS TIPO_MERCADO, NULL AS IDSETOR,        'ETF' AS NMSETOR, NULL AS IDSUBSETOR,        'ETF' AS NMSUBSETOR, NULL AS IDSEGMENTO,        'ETF' AS NMSEGMENTO, E.SITUACAO AS SITUACAOEMPRESA FROM TBETF_INDICE E
                    UNION ALL
                    SELECT 'BDR'    CATEGORIA, E.ID AS IDATIVO, E.CODIGO,     E.TIPO,     E.CODISIN, E.VLRPRECOFECHAMENTO, E.VLRPRECOANTERIOR, E.VLRVARIACAO, E.DATAHORAALTERACO, E.SITUACAO AS SITUACAOATIVO, E.ID AS IDEMPRESA, E.NOME,        E.NOME AS NOMERESUMIDO,         E.RAZAOSOCIAL,                       E.CNPJ,     E.CODCVM, '' AS SITE,   E.TIPO AS TIPO_MERCADO,       E.IDSETOR, ST.DESCRICAO AS NMSETOR,       E.IDSUBSETOR, SB.DESCRICAO AS NMSUBSETOR,       E.IDSEGMENTO, SG.DESCRICAO AS NMSEGMENTO, E.SITUACAO AS SITUACAOEMPRESA FROM TBBDR_EMPRESA E JOIN TBBDR_EMPRESA_SETOR ST ON (ST.ID = E.IDSETOR) JOIN TBBDR_EMPRESA_SUBSETOR SB ON (SB.ID = E.IDSUBSETOR) JOIN TBBDR_EMPRESA_SEGMENTO SG ON (SG.ID = E.IDSEGMENTO)
                    UNION ALL
                    SELECT 'CRIPTO' CATEGORIA, E.ID AS IDATIVO, E.CODIGO, '' AS TIPO, '' AS CODISIN, E.VLRPRECOFECHAMENTO, E.VLRPRECOANTERIOR, E.VLRVARIACAO, E.DATAHORAALTERACO, E.SITUACAO AS SITUACAOATIVO, E.ID AS IDEMPRESA, E.NOME,        E.NOME AS NOMERESUMIDO, E.NOME AS RAZAOSOCIAL, '00.000.000/0000-00' AS CNPJ, '' AS CODCVM, '' AS SITE, 'CRIPTO' AS TIPO_MERCADO, NULL AS IDSETOR,     'CRIPTO' AS NMSETOR, NULL AS IDSUBSETOR,     'CRIPTO' AS NMSUBSETOR, NULL AS IDSEGMENTO,     'CRIPTO' AS NMSEGMENTO, E.SITUACAO AS SITUACAOEMPRESA FROM TBCRIPTO_EMPRESA E
                    ORDER BY CATEGORIA, CODIGO
                """
                cursor.execute(query)
                result = cursor.fetchall()
                lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CATEGORIA')
            collection.create_index('CODIGO')
            collection.create_index('CODISIN')
            collection.create_index('NOME')
            collection.create_index('NOMERESUMIDO')
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('IDATIVO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('CODISIN', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('NOME', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('NOMERESUMIDO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('IDATIVO', pymongo.ASCENDING), ('SITUACAOATIVO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('SITUACAOATIVO', pymongo.ASCENDING)])
            collection.create_index('SITUACAOATIVO')
            collection.create_index([('SITUACAOATIVO', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('SITUACAOEMPRESA', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('SITUACAOEMPRESA', pymongo.ASCENDING), ('NOMERESUMIDO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('SITUACAOEMPRESA', pymongo.ASCENDING), ('NOME', pymongo.ASCENDING)])

        # collection = get_collection_empresa(db=db)

        # # ACAO - NOME - RAIZEN
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'ACAO', 'NOME': 'RAIZEN'})  # Done in 0.06s - 0:00:00.064183
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["NOME"]}')

        # # ACAO - CODIGO - MOSI3
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'ACAO', 'CODIGO': 'MOSI3'}) #  Done in 0.00s - 0:00:00.002964
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["CODIGO"]}')

        # # FII - NOME - FII HAZ
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'FII', 'NOME': 'FII HAZ'})  # Done in 0.04s - 0:00:00.039146
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["NOME"]}')

        # # FII - CODIGO - FLMA11
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'FII', 'CODIGO': 'FLMA11'}) #  Done in 0.00s - 0:00:00.003097
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["CODIGO"]}')

        # # ETF - NOME - Trend ETF OURO Fundo de Índice
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'ETF', 'NOME': 'Trend ETF OURO Fundo de Índice'})  # Done in 0.06s - 0:00:00.058358
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["NOME"]}')

        # # ETF - CODIGO - XMAL11
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'ETF', 'CODIGO': 'XMAL11'}) #  Done in 0.01s - 0:00:00.007785
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["CODIGO"]}')


        # # BDR - NOME - BKR US TREAS
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'BDR', 'NOME': 'BKR US TREAS'})  # Done in 0.06s - 0:00:00.063479
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["NOME"]}')

        # # BDR - CODIGO - S2TW34
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'BDR', 'CODIGO': 'S2TW34'}) #  Done in 0.00s - 0:00:00.002934
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["CODIGO"]}')

        # # CRIPTO - NOME - Polkadot
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'CRIPTO', 'NOME': 'Polkadot'})  #  Done in 0.05s - 0:00:00.051656
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["NOME"]}')

        # # CRIPTO - CODIGO - SOL/BRL
        # start_time_teste = time.perf_counter() 
        # result = collection.find_one({'CATEGORIA': 'CRIPTO', 'CODIGO': 'SOL/BRL'}) #  Done in 0.00s - 0:00:00.002523
        # end_time_teste = time.perf_counter() - start_time_teste
        # logger.warning(f'Done in {end_time_teste:.2f}s - {dt.timedelta(seconds=end_time_teste)} - {result["CATEGORIA"]} - {result["CODIGO"]}')

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


def migrar_empresa_cotacoes(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_cotacoes(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                #  ACAO

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBEMPRESA_ATIVOCOTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - ACAO = {len(tabelas)}") 

                lista = []
                for tabela in tabelas:
                    # logger.info(f"{tabela['TABLE_NAME']=} - {tabela['TABLE_NAME'].replace('TBEMPRESA_ATIVOCOTACAO_', '')=}") 
                    cursor.execute(f"SELECT 'ACAO' as CATEGORIA, '{tabela['TABLE_NAME'].replace('TBEMPRESA_ATIVOCOTACAO_', '')}' as CODIGO, DATA, COTACAO, VARIACAO FROM {tabela['TABLE_NAME']} ORDER BY DATA")
                    result = cursor.fetchall()
                    lista += [convert_decimal(row) for row in result]  # lista = [row for row in result]
                logger.info(f"Total MySQL - ACAO = {len(lista)}") 
                if lista: collection.insert_many(lista)

                #  FII

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBFII_FUNDOIMOB_COTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - FII = {len(tabelas)}") 

                lista = []
                for tabela in tabelas:
                    # logger.info(f"{tabela['TABLE_NAME']=} - {tabela['TABLE_NAME'].replace('TBFII_FUNDOIMOB_COTACAO_', '')=}") 
                    cursor.execute(f"SELECT 'FII' as CATEGORIA, '{tabela['TABLE_NAME'].replace('TBFII_FUNDOIMOB_COTACAO_', '')}' as CODIGO, DATA, COTACAO, VARIACAO FROM {tabela['TABLE_NAME']} ORDER BY DATA")
                    result = cursor.fetchall()
                    lista += [convert_decimal(row) for row in result]  # lista = [row for row in result]
                logger.info(f"Total MySQL - FII = {len(lista)}") 
                if lista: collection.insert_many(lista)

                #  ETF

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBETF_INDICE_COTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - ETF = {len(tabelas)}") 

                lista = []
                for tabela in tabelas:
                    # logger.info(f"{tabela['TABLE_NAME']=} - {tabela['TABLE_NAME'].replace('TBETF_INDICE_COTACAO_', '')=}") 
                    cursor.execute(f"SELECT 'ETF' as CATEGORIA, '{tabela['TABLE_NAME'].replace('TBETF_INDICE_COTACAO_', '')}' as CODIGO, DATA, COTACAO, VARIACAO FROM {tabela['TABLE_NAME']} ORDER BY DATA")
                    result = cursor.fetchall()
                    lista += [convert_decimal(row) for row in result]  # lista = [row for row in result]
                logger.info(f"Total MySQL - ETF = {len(lista)}") 
                if lista: collection.insert_many(lista)

                #  BDR

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TTBBDR_EMPRESA_COTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - BDR = {len(tabelas)}") 

                lista = []
                for tabela in tabelas:
                    # logger.info(f"{tabela['TABLE_NAME']=} - {tabela['TABLE_NAME'].replace('TTBBDR_EMPRESA_COTACAO_', '')=}") 
                    cursor.execute(f"SELECT 'BDR' as CATEGORIA, '{tabela['TABLE_NAME'].replace('TTBBDR_EMPRESA_COTACAO_', '')}' as CODIGO, DATA, COTACAO, VARIACAO FROM {tabela['TABLE_NAME']} ORDER BY DATA")
                    result = cursor.fetchall()
                    lista += [convert_decimal(row) for row in result]  # lista = [row for row in result]
                logger.info(f"Total MySQL - BDR = {len(lista)}") 
                if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        if lista:
            collection.create_index('CODIGO')
            collection.create_index([('CODIGO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('CODIGO', pymongo.ASCENDING), ('DATA', pymongo.ASCENDING)])

        # collection = get_collection_empresa_cotacoes(db=db)
        # collection.delete_many({'CATEGORIA': 'ACAO', 'CODIGO': 'ITSA4'})
        # rows = collection.find({'CATEGORIA': 'ACAO', 'CODIGO': 'ITSA4', 'DATA': '20220405'})
        # rows = collection.find({'CATEGORIA': 'CRIPTO', 'CODIGO': 'ADA/BRL', 'DATA': '20220521'}).limit(10)
        # rows = collection.find({'CATEGORIA': 'ACAO', 'CODIGO': 'ITSA4', 'DATA': {'$gte': '20220221', '$lte': '20220521'}}).sort('DATA', 1)
        # row = collection.find({'CATEGORIA': 'ACAO', 'CODIGO': 'ITSA4', 'DATA': {'$gte': '20220221', '$lte': '20220521'}}).sort('COTACAO', -1).limit(1)  # max
        # row = collection.find_one(filter={'CATEGORIA': 'ACAO', 'CODIGO': 'ITSA4', 'DATA': {'$gte': '20220221', '$lte': '20220521'}}, sort=[("DATA", -1)], limit=1)  # max
        # logger.warning(f'{row}')
        # for row in rows:
        #     logger.warning(f'{row}') 
        
        # Localhost
        # ACAO = 1.791.632 - 506 TABELAS
        # FII =    232.442 - 207 TABELAS
        # ETF =     37.003 -  21 TABELAS
        # BDR =    393.277 - 726 TABELAS
        # MondoDB = 2.454.354 - 00:03:41.709630

        # DigitalOcean
        # ACAO = 1809466 - 559 TABELAS
        # FII =    252141 - 283 TABELAS
        # ETF =     40582 -  62 TABELAS
        # BDR =    549567 - 811 TABELAS
        # MondoDB = 2651756 - 0:11:09.824658

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_cotacoes_drop_table(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                #  ACAO

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBEMPRESA_ATIVOCOTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - ACAO = {len(tabelas)}") 

                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE {tabela['TABLE_NAME']}")

                #  FII

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBFII_FUNDOIMOB_COTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - FII = {len(tabelas)}") 

                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE {tabela['TABLE_NAME']}")

                #  ETF

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBETF_INDICE_COTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - ETF = {len(tabelas)}") 

                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE {tabela['TABLE_NAME']}")

                #  BDR

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TTBBDR_EMPRESA_COTACAO_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - BDR = {len(tabelas)}") 

                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE {tabela['TABLE_NAME']}")

                #  CEI OPER

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBCEI_OPER_USER_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - CEI OPER = {len(tabelas)}") 

                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE {tabela['TABLE_NAME']}")

                #  CEI PROV

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBCEI_PROV_USER_%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - CEI PROV = {len(tabelas)}") 

                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE {tabela['TABLE_NAME']}")

                #  EMPRESA FINAN

                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'TBEMPRESA_FINAN%' ORDER BY TABLE_NAME")
                result = cursor.fetchall()
                tabelas = [row for row in result] 
                logger.info(f"Total Tabelas - EMPRESA FINAN = {len(tabelas)}") 

                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE {tabela['TABLE_NAME']}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_fatos(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection = get_collection_empresa_fatos(db=db)
        collection.delete_many({})

        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:

                query = """
                    SELECT 'ACAO' CATEGORIA, F.ID AS IDFATO, F.IDEMPRESA, F.NMEMPRESA, F.DATA_ENV, F.DATA_REF, F.PROTOCOLO, F.LINK, F.ASSUNTO, F.CONTEUDO, F.SITUACAO FROM TBEMPRESA_FATORELEVANTE F
                    UNION ALL
                    SELECT 'FII' CATEGORIA, F.ID AS IDFATO, F.IDFUNDO AS IDEMPRESA, F.NMFUNDO AS NMEMPRESA, F.DATA_ENV, F.DATA_REF, F.PROTOCOLO, F.LINK, F.ASSUNTO, F.CONTEUDO, F.SITUACAO FROM TBFII_FUNDOIMOB_FATORELEVANTE F
                    UNION ALL
                    SELECT 'ETF' CATEGORIA, F.ID AS IDFATO, F.IDINDICE AS IDEMPRESA, F.NMINDICE AS NMEMPRESA, F.DATA_ENV, F.DATA_REF, F.PROTOCOLO, F.LINK, F.ASSUNTO, F.CONTEUDO, F.SITUACAO FROM TBETF_FATORELEVANTE F
                    UNION ALL
                    SELECT 'BDR' CATEGORIA, F.ID AS IDFATO, F.IDBDR AS IDEMPRESA, F.NMEMPRESA, F.DATA_ENV, F.DATA_REF, F.PROTOCOLO, F.LINK, F.ASSUNTO, F.CONTEUDO, F.SITUACAO FROM TBBDR_EMPRESA_FATORELEVANTE F
                    ORDER BY CATEGORIA, IDFATO
                """
                cursor.execute(query)
                result = cursor.fetchall()
                lista = [row for row in result] 
                logger.info(f"Total MySQL = {len(result)}") 

        if lista: collection.insert_many(lista)

        logger.info(f"Total MondoDB = {collection.count_documents({})}")

        result_delete = collection.delete_many({'DATA_REF': {"$lt": '20220201'}})  # $lt <
        logger.info(f"{result_delete.deleted_count=}")

        if lista:
            collection.create_index('CATEGORIA')
            collection.create_index('LINK')
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('IDFATO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('IDEMPRESA', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('LINK', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('DATA_ENV', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('IDEMPRESA', pymongo.ASCENDING), ('DATA_ENV', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])
            collection.create_index([('CATEGORIA', pymongo.ASCENDING), ('IDEMPRESA', pymongo.ASCENDING), ('DATA_ENV', pymongo.ASCENDING), ('PROTOCOLO', pymongo.ASCENDING), ('SITUACAO', pymongo.ASCENDING)])

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_fatos_ajustar_protocolo(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
    try:

        client = get_client(mongo_uri=mongo_uri)
        db = get_database(client=client)

        collection_empresa_fatos = get_collection_empresa_fatos(db=db)

        fatos = collection_empresa_fatos.find({}) 
        
        total = fatos.count()
        logger.warning(f'{total=}')

        for fato in fatos:
            try:
                collection_empresa_fatos.update_many({"_id": ObjectId(fato['_id'])}, {"$set": {"PROTOCOLO": int(fato['PROTOCOLO'])}})
            except Exception as e:
                logger.error(f'Falha Geral: "{str(e)}"')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def migrar_empresa_xxxxxxxx(mongo_uri: str, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
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