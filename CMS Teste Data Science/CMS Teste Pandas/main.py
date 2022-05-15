import chunk
from fileinput import filename
from django.forms import PasswordInput
from loguru import logger
import datetime as dt
import time
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import warnings
from dotenv import load_dotenv


def teste_01_pandas_excel():
    try:

        def read_excel() -> pd.DataFrame:
            df = pd.read_excel(io='Pasta1.xlsx', sheet_name='Planilha1', header=None, names=['col1', 'col2', 'col3'], index_col=None, usecols=['col1','col2', 'col3'])
            return df

        def save_excel(df: pd.DataFrame) -> None:
            df.to_excel('teste.xlsx', sheet_name='Teste', na_rep='#N/A', header=True, index=False)

        df = read_excel()
        save_excel(df=df)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_02_pandas_csv_to_bd():
    try:

        # Memory Error - Somente par arquivos acima de 2GB
        # 'cp1252' = ok  # 'ISO 8859-1' /  'ISO-8859-1' = ok

        engine = create_engine("sqlite:///banco.db", echo=False, future=False) # True
        chunksize, i, j = 10_000, 0, 0
        filename =  r'C:\Users\chris\Desktop\5m CC Records.csv' 

        for df in pd.read_csv(filepath_or_buffer=filename, sep=',', encoding='cp1252', nrows=None, chunksize=chunksize, iterator=True):
            df = df.rename(columns = {c: c.replace(' ','') for c in df.columns}) # remove space in columns names
            df.index += j
            df.to_sql(name='data_user', con=engine, if_exists='append')
            j = df.index[-1] + 1
            i += 1
            logger.info(f'Index {i} - Total {j:,2f}')
            if i > 10: break

        # with engine.begin() as conn:
        # with engine.connect() as conn:
        sql = 'SELECT * FROM data_user WHERE CreditLimit = 12000 '
        df = pd.read_sql_query(sql=sql, con=engine)
        logger.info(f'{df}')
        logger.info(f'{df.columns}')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')




def teste_03_pandas_tratar_dados():
    try:

        # Leitura, DadosAusentes, RemoverDuplicados, Transformar, Dicretização, RemoverDescrepantes

        filename = './COVID19 cases Toronto.csv'
        filename = r'C:\\Users\\chris\\Desktop\\CMS Python\\CMS Arquivos para Testes\\COVID19 cases Toronto.csv'
        df = pd.read_csv(filepath_or_buffer=filename, sep=',')

        # logger.info(f'{df}')  # [14911 rows x 17 columns]
        # logger.info(f'{df.info()}')
        # logger.info(f'{df.describe()}')
        # logger.info(f'{df.describe(include="all")}')
        # logger.info(f'{df.columns}')
        
        # _id,Outbreak Associated,Age Group,Neighbourhood Name,FSA,Source of Infection,
        # Classification,Episode Date,Reported Date,Client Gender,Outcome,Currently Hospitalized,
        # Currently in ICU,Currently Intubated,Ever Hospitalized,Ever in ICU,Ever Intubated

        # logger.info(f'Dados Nulos')
        # logger.info(f'{df.isnull()}')
        # logger.info(f'{df.isnull().sum()}')
        
        # logger.info(f'Adicionando uma linha com todos os dados Nulos')
        # df = df.append(pd.Series(), ignore_index=True)
        # logger.info(f'{df.tail()}')

        # logger.info(f'Adicionando uma coluna nula para todas as linhas')
        # df['Nulo'] = np.NAN
        # df.dropna(axis=1, how='all') # xis=0-Linhas # xis=1-Colunas # deletar a linha onde tem coluna q tds os valores seja nulos

        # logger.info(f'Dropar Dados Nulos')
        shape_before = df.shape[0]
        # shape_curr = df.dropna().shape[0] # pelo menos uma coluna seja Nula
        # shape_curr = df.dropna(how='all').shape[0] # todos os campos seja nulos
        shape_curr = df.dropna(thresh=2).shape[0] # deletar as linhas q tenha pelo menos 2 colunas com valor nulos
        # shape_curr = df.drop_duplicates().shape[0]
        # shape_curr = df.drop_duplicates(subset=['FSA', 'Age Group' ,'Outbreak Associated']).shape[0]
        # shape_curr = df.drop_duplicates(subset=['FSA', 'Age Group' ,'Outbreak Associated'], keep='last').shape[0]
        # shape_curr = df.drop(df[df['day'] < 20].index).shape[0]
        logger.info(f'{shape_before} linhas antes')
        logger.info(f'{shape_curr} linhas depois')
        logger.info(f'{shape_before-shape_curr} linhas removidas')
        logger.info(f'{round(((shape_before-shape_curr)/shape_before)*100, 2)} % removido')

        # logger.info(f'Preencher linha vazia')
        # df.fillna(value="")
        # df.fillna(value={'Age Group': 'Não tem', 'Classification': 'Sem Status'})
        # df.fillna(method='ffill')
        # df.fillna(value=df.mean())
        # df[df.duplicated()]

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_02_pandas_redis():
    import os
    import pandas as pd
    import redis
    RC = redis.Redis(host=os.environ.get('REDIS_HOST'), charset='utf-8', decode_responses=True)
    df = pd.DataFrame()
    for key in RC.keys():
        value = RC.hgetall(key)
        # print(value)
        value['login'] = key
        df = df.append(value, ignore_index=True)
        for k in ['public_repos', 'public_gists', 'followers', 'following']:
            df[k] = df[k].astype(int)
    # print(df)
    # df.sum()



def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # pd.set_option('display.precision', 2)
        # pd.set_option('float_format', '{:.3f}'.format)
        # pd.reset_option('^display.', silenct=True)

        # teste_01_pandas_excel()
        # teste_02_pandas_csv_to_bd()
        teste_03_pandas_tratar_dados()
        # teste_05_pandas_redis()

        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade xxxxxxx
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
# python3 main.py  
# pypy3 main.py
