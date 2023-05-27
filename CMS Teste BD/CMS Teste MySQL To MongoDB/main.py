from loguru import logger
import time
import datetime as dt
from dynaconf import Dynaconf
from mongo import *
from migrar_admin import *
from migrar_empresa import *
from migrar_outros import *
from migrar_user import *


def main():
    logger.info(f'Inicio') 
    try:

        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        settings = Dynaconf(load_dotenv=True, environments=True, envvar_prefix="CMS_TNB")

        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        # DigitalOcean

        mysql_host, mysql_user, mysql_password, mysql_database, mongo_uri = settings.MYSQL_HOST_DIGITAL_OCEAN, settings.MYSQL_USER_DIGITAL_OCEAN, settings.MYSQL_PASS_DIGITAL_OCEAN, settings.MYSQL_DB_DIGITAL_OCEAN, settings.MONGODB_URI_DIGITAL_OCEAN
        logger.info(f'{mysql_host} - {mysql_user} - {mysql_password} - {mysql_database} - {mongo_uri}')

        # usuario        
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
        # migrar_usuario_nota_corretagem(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_nota_corretagem_data(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_nota_corretagem_oper(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_nota_corretagem_ajustar_id(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_carteira_projecao(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_carteira_projecao_item(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_carteira_projecao_ajustar_id(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_cei(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_cei_oper(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_cei_prov(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_cei_ajustar_id(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_empresa_fatos(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_usuario_empresa_proventos(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)

        # empresa
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
        # migrar_empresa_cotacoes(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_cotacoes_drop_table(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_admin(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_setores(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_fatos(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_fatos_ajustar_protocolo(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_empresa_proventos(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)

        # outros    
        # migrar_noticia(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_admin_log_erros(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        # migrar_admin_fatos(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)

        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        # Localhost

        # mysql_host, mysql_user, mysql_password, mysql_database, mongo_uri = settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASS, settings.MYSQL_DB, settings.MONGODB_URI
        # logger.info(f'{mysql_host} - {mysql_user} - {mysql_password} - {mysql_database} - {mongo_uri}')

        # migrar_usuario_aluguel(mongo_uri=mongo_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)

        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        # Desenv

        client = get_client(mongo_uri=mongo_uri)
        db     = get_database(client=client)

        # id_usuario    = 2  # 2-CMS
        # id_corretora  = 3  # 3-MODAL
        # dt_ini        = '20220201'
        # dt_fim        = '20220519'
        # tipo_usuario  = 'A'   # I-Investidor  # A-Administrador
        # id_comentario = 784  # 784 # 796 # 800
        # import uuid # uuid.uuid1()  # uuid.uuid4()  # uuid.uuid4().hex  # uuid.uuid4()  # UUID = uuid.uuid1()  UUID.int

        collection = get_collection_usuarios(db=db)
        row = collection.find_one({'EMAIL': 'falcao.ila@gmail.com'})
        if row: 
            logger.info(row)
            # collection.update_one({"_id": row["_id"]}, {"$set": {"SENHA": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3", "TENTATIVA": 0, "SITUACAO": 'A'}})
            # 8b128de4ca8a7bfc7de724c528bb5efebc053cae841d799b344d41a208e32d85


        connection = get_connection_mysql(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database)
        with connection:
            with connection.cursor() as cursor:
                query = """ SELECT * FROM TBUSUARIO WHERE ID = 486 """
                cursor.execute(query) # ID, NOME, EMAIL, SENHA, DTREGISTRO, TENTATIVA, TIPO, SITUACAO, FOTO, CHATID, HASH
                result = cursor.fetchall()
                for row in result:
                    logger.info(row)
                    # query = "UPDATE TBUSUARIO SET SENHA = '', TENTATIVA = 0, SITUACAO = 'A' WHERE ID = 486 "
                    # cursor.execute(sql, val)
                    # connection.commit()


        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


if __name__ == '__main__':
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade mysql-connector-python
# python -m pip install --upgrade PyMySQL
# python -m pip install --upgrade python-dotenv
# python -m pip install --upgrade dynaconf
# python -m pip install --upgrade pymongo
# python -m pip install --upgrade loguru
# python -m pip install --upgrade numpy
# python main.py

# py -m pip install --upgrade pip
# py -m pip install --upgrade mysql-connector-python
# py -m pip install --upgrade PyMySQL
# py -m pip install --upgrade python-dotenv
# py -m pip install --upgrade dynaconf
# py -m pip install --upgrade pymongo
# py -m pip install --upgrade loguru
# py -m pip install --upgrade numpy
# py main.py
