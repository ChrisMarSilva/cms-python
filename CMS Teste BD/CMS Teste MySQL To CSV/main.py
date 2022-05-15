from loguru import logger
import time
import datetime as dt
from dynaconf import Dynaconf
import pymysql
import pymysql.cursors
import csv
import pandas as pd
import shutil
import zipfile
import os


def gerar_backup_tabela(mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str, tabela: str):
    try:

        connection = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:

                # GET COLUMNS

                # cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tabela}' ORDER BY ORDINAL_POSITION")
                # result = cursor.fetchall()
                # logger.info(f"{len(result)=}") 

                # cols = [row['COLUMN_NAME'] for row in result] 
                # logger.info(f"{len(cols)=}") 
                # logger.info(f"{cols=}") 
                # # [{'COLUMN_NAME': 'ID', 'DATA_TYPE': 'int'}, {'COLUMN_NAME': 'NOME', 'DATA_TYPE': 'varchar'}, {'COLUMN_NAME': 'EMAIL', 'DATA_TYPE': 'varchar'}, {'COLUMN_NAME': 'SENHA', 'DATA_TYPE': 'varchar'}, {'COLUMN_NAME': 'DTREGISTRO', 'DATA_TYPE': 'varchar'}, {'COLUMN_NAME': 'TENTATIVA', 'DATA_TYPE': 'int'}, {'COLUMN_NAME': 'TIPO', 'DATA_TYPE': 'varchar'}, {'COLUMN_NAME': 'SITUACAO', 'DATA_TYPE': 'varchar'}, {'COLUMN_NAME': 'FOTO', 'DATA_TYPE': 'varchar'}, {'COLUMN_NAME': 'CHATID', 'DATA_TYPE': 'varchar'}]

                # GET ROWS

                cursor.execute(f"SELECT * FROM {tabela}")
                result = cursor.fetchall()
                # logger.info(f"{len(result)=}") 

                # cols = list()
                # for i in cursor.description:
                #     cols.append(i[0])
                cols = [i[0] for i in cursor.description]
                # logger.info(f"{len(cols)=}") 
                # logger.info(f"{cols=}") 

                # rows = [row for row in result] 
                rows = [[row[col] if row[col] else '' for col in cols] for row in result] 
                # logger.info(f"{len(rows)=}") 
                # logger.info(f"{rows[5]=}") 

                # [2, 'Chris MarSil', 'email@gmail.com', '003f37118f2d54ad5b494e103c7f0125be9def9f1a1423a91a17153f8e1842a0', '20180101', 0, 'A', 'A', 'user_2_78ee87d13d24956ebad82e9d0dbc44aa.jpg', '452513294']
                # [9, 'Decio Vitorino Filho', 'dvitorinofilho@gmail.com', '29d991950f0c8c4006cefc8c5747c162fd78aa743cf2f08bb4fe9fe65e06f665', '20180717', 0, 'I', 'A', None, None]
                # [9, 'Decio Vitorino Filho', 'dvitorinofilho@gmail.com', '29d991950f0c8c4006cefc8c5747c162fd78aa743cf2f08bb4fe9fe65e06f665', '20180717', '', 'I', 'A', '', '']

                file = f"./dump/{tabela}.csv"

                # with open(file=file, mode='w', encoding='utf-8', newline='') as csvfile:
                #     csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
                #     csvwriter.writerow(cols)
                #     csvwriter.writerows(rows)
                #     # for row in rows:
                #     #     csvwriter.writerow(row)

                data = pd.DataFrame(data=rows, columns=cols)
                data.to_csv(path_or_buf=file, index=False, sep=",")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    logger.info(f'Inicio') 
    try:

        start_time = time.perf_counter()

        settings = Dynaconf(load_dotenv=True, environments=True, envvar_prefix="CMS_TNB")
        mysql_host, mysql_user, mysql_password, mysql_database = settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASS, settings.MYSQL_DB
        logger.info(f'MYSQL   = {mysql_host} - {mysql_user} - {mysql_password} - {mysql_database}')

        tabelas = [
            "TBBDR_EMPRESA_SEGMENTO",
            "TBBDR_EMPRESA_SETOR",
            "TBBDR_EMPRESA_SUBSETOR",
            "TBEMPRESA_SEGMENTO",
            "TBEMPRESA_SETOR",
            "TBEMPRESA_SUBSETOR",
            "TBFII_FUNDOIMOB_TIPO",
            "TBEMPRESA",
            "TBEMPRESA_ATIVO",
            "TBEMPRESA_FATORELEVANTE",
            "TBEMPRESA_PROVENTO",
            "TBEMPRESA_FINAN",
            "TBEMPRESA_FINAN_AGENDA",
            "TBEMPRESA_FINAN_BPA_ANUAL",
            "TBEMPRESA_FINAN_BPA_TRIMESTRAL",
            "TBEMPRESA_FINAN_BPP_ANUAL",
            "TBEMPRESA_FINAN_BPP_TRIMESTRAL",
            "TBEMPRESA_FINAN_DFC_ANUAL",
            "TBEMPRESA_FINAN_DFC_TRIMESTRAL",
            "TBEMPRESA_FINAN_DRE_ANUAL",
            "TBEMPRESA_FINAN_DRE_TRIMESTRAL",
            "TBFII_FUNDOIMOB_ADMIN",
            "TBFII_FUNDOIMOB",
            "TBFII_FUNDOIMOB_FATORELEVANTE",
            "TBFII_FUNDOIMOB_PROVENTO",
            "TBETF_INDICE",
            "TBETF_FATORELEVANTE",
            "TBBDR_EMPRESA",
            "TBBDR_EMPRESA_FATORELEVANTE",
            "TBBDR_EMPRESA_PROVENTO",
            "TBCRIPTO_EMPRESA",
            "TBUSUARIO",
            "TBUSUARIO_LOG",
            "TBUSUARIO_HASH",
            "TBUSUARIO_CONFIG",
            "TBLOGERRO",
            "TBCEI",
            "TBCORRETORA_LISTA",
            "TBCORRETORA",
            "TBALERTA",
            "TBALERTA_ASSINATURA",
            "TBALERTA_NOTICIA",
            "TBAPURACAO",
            "TBAPURACAO_CALCULADA",
            "TBALUGUEL_ATIVO",
            "TBLANCAMENTO",
            "TBOPERACAO",
            "TBPROVENTO",
            "TBFII_LANCAMENTO",
            "TBFII_PROVENTO",
            "TBETF_LANCAMENTO",
            "TBETF_OPERACAO",
            "TBBDR_LANCAMENTO",
            "TBBDR_OPERACAO",
            "TBBDR_PROVENTO",
            "TBCRIPTO_LANCAMENTO",
            "TBUSUARIO_ACOMP_GRUPO",
            "TBUSUARIO_ACOMP_ATIVO",
            "TBUSUARIO_ACOMP_BDR",
            "TBUSUARIO_ACOMP_CRIPTO",
            "TBUSUARIO_ACOMP_FUNDO",
            "TBUSUARIO_ACOMP_INDICE",
            "TBCARTEIRA",
            "TBCARTEIRA_ATIVO",
            "TBCARTEIRA_BDR",
            "TBCARTEIRA_COTAS",
            "TBCARTEIRA_CRIPTO",
            "TBCARTEIRA_FUNDO",
            "TBCARTEIRA_INDICE",
            "TBCARTEIRA_PROJECAO",
            "TBCARTEIRA_PROJECAO_ITEM",
            "TBFII_FUNDOIMOB_FATORELEVANTE_ATIVO",
            "TBFII_FUNDOIMOB_PROVENTO_ATIVO",
            "TBEMPRESA_FATORELEVANTE_ATIVO",
            "TBEMPRESA_PROVENTO_ATIVO",
            "TBETF_FATORELEVANTE_ATIVO",
            "TBBDR_EMPRESA_FATORELEVANTE_ATIVO",
            "TBBDR_EMPRESA_PROVENTO_ATIVO",
            "TBNOTA_CORRETAGEM",
            "TBNOTA_CORRETAGEM_DATA",
            "TBNOTA_CORRETAGEM_OPER",
        ]

        for idx, tabela in enumerate(tabelas):
            logger.warning(f"{idx+1}/{len(tabelas)} - {tabela}")
            gerar_backup_tabela(mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_database=mysql_database, tabela=tabela)

        # file = f'./dump/{tabela}.csv'
        # file = f'./dump/TBUSUARIO.csv'

        # df = pd.read_csv(file, index_col=False, delimiter=',', header=0)
        # logger.info(f"{df}")

        # with open(file=file, mode='r', encoding='utf-8', newline='') as csv_file:
        #     csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        #     for row in csv_reader:
        #         print(', '.join(row)) # print(row)

        # shutil.make_archive(base_name='./dump', format='zip', root_dir='./dump')

        # path = 'dump/'
        # with zipfile.ZipFile(file='dump2.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
        #     for root, dirs, files in os.walk(path):
        #         for file in files:
        #             zipf.write(os.path.join(root, file),  os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

        end_time = time.perf_counter() - start_time
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
