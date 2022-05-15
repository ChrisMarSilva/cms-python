from cProfile import label
from distutils.command.build_scripts import first_line_re
from tokenize import group
from loguru import logger
import datetime as dt
import time
import timeit
import sys
import pandas as pd
import numpy as np
import swifter
import matplotlib.pyplot as plt
import requests
import os
from joblib import Parallel, delayed
import asyncio
import platform
import dask.dataframe as dd 
import multiprocessing as mp
from dotenv import load_dotenv


def define_period(str_datime, format_time = '%m/%d/%y %H:%M'):
    try:
        obj_datetime = time.strptime(str_datime, format_time)
    except:
        return 'undefined'
    if obj_datetime.tm_hour < 12:
        return 'AM'
    else:
        return 'PM'


def teste_01_normal() -> None:

    logger.info(f'Carregando dados')
    df_tmp = pd.read_csv(filepath_or_buffer='sales_data.csv', sep=',', index_col=0)
    # logger.info(f'{df_tmp}')

    logger.info(f'Copiando dados')
    df = df_tmp.copy()
    # logger.info(f'{df.info()}')  # 185.950 linhas # 8 columns # memory usage: 12.8+ MB
    
    for idx in range(3):
        logger.info(f'Append dados #{idx+1}')
        df = df.append(df)
    df = df.reset_index(drop=True)
    logger.info(f'{df.info()}')  # 1.487.600 # memory usage: 90.8+ MB

    # logger.info(f"{df.loc[0, 'Order Date']}")
    # logger.info(f"{time.strptime(df.loc[0, 'Order Date'], '%m/%d/%y %H:%M')}")
    # logger.info(f"{time.strptime(df.loc[0, 'Order Date'], '%m/%d/%y %H:%M').tm_hour}")

    logger.info(f'apply - Criando coluna period')
    start_time_period = time.perf_counter()
    #df['period1'] = df.apply(lambda row: define_period(str_datime=row['Order Date'], format_time='%m/%d/%y %H:%M'), axis=1)
    df['period1'] = df['Order Date'].apply(lambda x: define_period(str_datime=x), axis=1)
    end_time_period = time.perf_counter() - start_time_period
    logger.info(f'apply - Coluna criada em {end_time_period:.2f}s - {dt.timedelta(seconds=end_time_period)}')
    # logger.info(f'{df}')

    logger.info(f'swifter - Criando coluna period')
    start_time_period = time.perf_counter()
    # df['period2'] = df.swifter.apply(lambda row: define_period(str_datime=row['Order Date'], format_time='%m/%d/%y %H:%M'), axis=1)
    df['period2'] = df['Order Date'].swifter.apply(lambda x: define_period(str_datime=x), axis=1)
    end_time_period = time.perf_counter() - start_time_period
    logger.info(f'swifter - Coluna criada em {end_time_period:.2f}s - {dt.timedelta(seconds=end_time_period)}')
    # logger.info(f'{df}')


def teste_02_benchmark() -> None:

    logger.info(f'Carregando dados')
    df_tmp = pd.read_csv(filepath_or_buffer='sales_data.csv', sep=',', index_col=0)
    # logger.info(f'{df_tmp}')
    
    logger.info(f'Copiando dados')
    df = df_tmp.copy()
    # logger.info(f'{df.info()}')  # 185.950 linhas # 8 columns # memory usage: 12.8+ MB

    num_exec = 1
    exec_pandas = np.zeros(num_exec)
    exec_swifter = np.zeros(num_exec)
    exec_dask = np.zeros(num_exec)
    dataset_len = np.zeros(num_exec)

    for idx in range(num_exec):
        logger.info(f'Teste #{idx+1}')

        dataset_len[idx] = len(df)

        logger.info(f'Teste #{idx+1} - Apply')
        start_time = time.perf_counter()
        df['period'] = df['Order Date'].apply(lambda x: define_period(str_datime=x))
        exec_pandas[idx] = time.perf_counter() - start_time

        logger.info(f'Teste #{idx+1} - Swifter')
        start_time = time.perf_counter()
        df['period'] = df['Order Date'].swifter.apply(lambda x: define_period(str_datime=x))
        exec_swifter[idx] = time.perf_counter() - start_time

        logger.info(f'Teste #{idx+1} - Dask')
        start_time = time.perf_counter()
        ddf = dd.from_pandas(df, npartitions=2) # 24
        df['period'] = ddf['Order Date'].apply(lambda x: define_period(str_datime=x), meta=ddf)
        # df['period'] = ddf.map_partitions(lambda df: df['Order Date'].apply((lambda x: define_period(str_datime=x)), axis=1)).compute(scheduler='processes')  
        exec_dask[idx] = time.perf_counter() - start_time

        logger.info(f'Teste #{idx+1} - Append')
        df = df.append(df)
        df = df.reset_index(drop=True)
    
    logger.info(f'Show Img')
    plt.figure(figsize=(7,5))
    plt.plot(dataset_len, exec_pandas, label='Apply')
    plt.plot(dataset_len, exec_swifter, label='Swifter')
    plt.plot(dataset_len, exec_dask, label='Dask')
    plt.ylabel('Runtime (s)')
    plt.xlabel('Number of Rows')
    plt.legend()
    plt.show()
    # plt.savefig('test.png')  # png  # pdf
    

def teste_03_joblib_lento() -> None:

    # logger.info(f'Inicio - joblib - lento') 
    start_time = time.perf_counter()

    arquivos = os.listdir()
    for arquivo in arquivos:
        if "xlsx" in arquivo:
            tabela = pd.read_excel(io=arquivo)
            faturamento = tabela["Valor Final"].sum()
            # logger.info(f"Faturamento da Loja {arquivo.replace('.xlsx', '')} foi de R${faturamento:,.2f}")

    end_time = time.perf_counter() - start_time
    logger.info(f"Fim - joblib - lento - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


def teste_04_joblib_rapido() -> None:

    # logger.info(f'Inicio - joblib - rapido') 
    start_time = time.perf_counter()

    def calcular_faturamento(arquivo: str):
        if "xlsx" in arquivo:
            tabela = pd.read_excel(io=arquivo)
            return f"Faturamento da Loja {arquivo.replace('.xlsx', '')} foi de R${tabela['Valor Final'].sum():,.2f}"

    arquivos = os.listdir()
    # resultado = Parallel(n_jobs=-1)(delayed(calcular_faturamento)(arquivo) for arquivo in arquivos)
    resultado = Parallel(n_jobs=2)(delayed(calcular_faturamento)(arquivo) for arquivo in arquivos)
    # logger.info(f'{resultado}')

    end_time = time.perf_counter() - start_time
    logger.info(f"Fim - joblib - rapido - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


async def teste_05_asyncio() -> None:

    # logger.info(f'Inicio - asyncio - rapido') 
    start_time = time.perf_counter()

    if platform.system() == 'Windows':
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def calcular_faturamento(arquivo: str):
        if "xlsx" in arquivo:
            tabela = pd.read_excel(io=arquivo)
            return f"Faturamento da Loja {arquivo.replace('.xlsx', '')} foi de R${tabela['Valor Final'].sum():,.2f}"

    arquivos = os.listdir()
    tasks = [asyncio.create_task(calcular_faturamento(arquivo=arquivo)) for arquivo in arquivos if "xlsx" in arquivo]
    resultado = await asyncio.gather(*tasks)
    # logger.info(f'{resultado}')

    end_time = time.perf_counter() - start_time
    logger.info(f"Fim - asyncio - rapido - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


def teste_06_single_thread_loop() -> None:
    
    logger.info(f"load")
    # filename = './small-cc-records.csv'
    filename = './5m CC Records.csv' # Done in 16.31s - 0:00:16.311717
    filename = './sales_data.csv'    # Done in  1.26s - 0:00:01.261020
    df = pd.read_csv(filepath_or_buffer=filename, encoding='windows-1252')
    # logger.info(f"{df}") # ,Order ID,Product,Quantity Ordered,Price Each,Order Date,Purchase Address,Month,City
    df['start-digits'] = None

    logger.info(f"{df.info()}")

    logger.info(f"loop")
    startTime = timeit.default_timer()
    for idx, row in enumerate(df.index):
        df_row = df.iloc[idx]
        first_digits_in_card_number = str(df_row["Order ID"])[:4]
        df.iloc[idx, 9] = first_digits_in_card_number
        
    logger.info(f"group")
    group_dataframe = df.groupby(['start-digits'])
    size_of_group = group_dataframe.size()
    logger.info(f"{size_of_group=}")
    logger.info(f"{group_dataframe.get_group('1765')=}")

    stopTime = timeit.default_timer() - startTime
    round_time = round(stopTime, 6)
    logger.info(f"Fim multiprocessing - {round_time:.2f}s - {dt.timedelta(seconds=round_time)}")


def teste_06_single_thread_apply() -> None:

    def card_handler(x):
        first_digits_in_card_number = str(x)[:4]
        return first_digits_in_card_number
    
    logger.info(f"load")
    # filename = './small-cc-records.csv'
    filename = './5m CC Records.csv' # Done in 16.31s - 0:00:16.311717
    filename = './sales_data.csv'    # Done in  1.26s - 0:00:01.261020
    df = pd.read_csv(filepath_or_buffer=filename, encoding='windows-1252')
    # logger.info(f"{df}") # ,Order ID,Product,Quantity Ordered,Price Each,Order Date,Purchase Address,Month,City
    df['start-digits'] = None

    logger.info(f"{df.info()}")

    logger.info(f"apply")
    startTime = timeit.default_timer()
    df['start-digits'] = df["Order ID"].apply(card_handler)

    logger.info(f"group")
    group_dataframe = df.groupby(['start-digits'])
    size_of_group = group_dataframe.size()
    logger.info(f"{size_of_group=}")
    logger.info(f"{group_dataframe.get_group('1765')=}")

    stopTime = timeit.default_timer() - startTime
    round_time = round(stopTime, 6)
    logger.info(f"Fim multiprocessing - {round_time:.2f}s - {dt.timedelta(seconds=round_time)}")



def card_handler(x):
    x['start-digits'] = x['Order ID'].apply(strip_digits)
    return x

def strip_digits(x):
    return str(x)[:4]
    
def teste_06_multi_thread() -> None:

    mp.set_start_method('spawn')

    cores = mp.cpu_count()
    partitions = cores * 10
    logger.info(f"{cores=}")
    logger.info(f"{partitions=}")

    logger.info(f"load")
    # filename = './small-cc-records.csv'
    # filename = './5m CC Records.csv' # Done in 16.31s - 0:00:16.311717
    filename = './sales_data.csv'    # Done in  1.26s - 0:00:01.261020
    df = pd.read_csv(filepath_or_buffer=filename, encoding='windows-1252')
    # logger.info(f"{df}") # ,Order ID,Product,Quantity Ordered,Price Each,Order Date,Purchase Address,Month,City
    df['start-digits'] = None
    # logger.info(f"{df.info()}")
    startTime = timeit.default_timer()

    def parallelize(dataframe, func):
        dataframe_split = np.array_split(dataframe, partitions) 
        with mp.Pool(cores) as p: 
            return pd.concat(p.map(func, dataframe_split), ignore_index=True)

    logger.info(f"parallelize")
    df = parallelize(df, card_handler)

    logger.info(f"group")
    group_dataframe = df.groupby(['start-digits'])
    size_of_group = group_dataframe.size()
    logger.info(f"{size_of_group=}")
    logger.info(f"{group_dataframe.get_group('1765')=}")

    stopTime = timeit.default_timer() - startTime
    round_time = round(stopTime, 6)
    logger.info(f"Fim multiprocessing - {round_time:.2f}s - {dt.timedelta(seconds=round_time)}")


def teste_07_modin() -> None:
    import modin.pandas as pd
    df = pd.read_csv("my_dataset.csv")


def main() -> None:
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # teste_01_normal()
        # teste_02_benchmark()

        # teste_03_joblib_lento()   # 1.78s
        # teste_04_joblib_rapido()  # 3.63s
        # asyncio.run(teste_05_asyncio())  # 1.84s

        # https://eforexcel.com/wp/downloads-17-sample-csv-files-data-sets-for-testing-credit-card/

        # teste_06_single_thread_loop()  # 89.31s - 0:01:29.305067
        # teste_06_single_thread_apply() #  0.34s - 0:00:00.341004
        teste_06_multi_thread()        #  7.47s - 0:00:07.467570
        # teste_07_modin()

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade swifter
# python -m pip install --upgrade matplotlib
# python -m pip install --upgrade joblib
# python -m pip install --upgrade openpyxl
# python -m pip install --upgrade dask 
# python -m pip install --upgrade "dask[complete]"
# python -m pip install --upgrade modin[all]
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
