from loguru import logger
import datetime as dt
import time
import os
os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"
# os.environ['HADOOP_HOME'] = "C:\\winutils\\hadoop-2.7.1\\bin"
# os.environ['SPARK_HOME']  = "C:\\winutils\\hadoop-2.7.1\\bin"
print('sss', os.getenv('PYSPARK_HADOOP_VERSION'))
import pyspark.pandas as ps
from dotenv import load_dotenv


def teste_01_spark():
    try:

        psdf = ps.range(10)
        pdf = psdf.to_pandas()
        logger.info(f'{pdf.values}') 

        # psdf = ps.DataFrame(range(10)) # Create a DataFrame with Pandas-on-Spark  
        # logger.info(f'{psdf}') 

        # # Convert a Pandas-on-Spark DataFrame into a Pandas DataFrame
        # pddf = psdf.to_pandas()
        # logger.info(f'{psdf}') 

        # logger.info(f'psdf={type(psdf)}')
        # logger.info(f'pddf={type(pddf)}') 



        # psdf = ps.DataFrame({'id': range(10)}, index=range(10)) # Create a pandas-on-Spark DataFrame with an explicit index.
        # sdf = psdf.to_spark(index_col='index') # Keep the explicit index.
        # sdf = sdf.filter("id > 5")  # Call Spark APIs
        # sdf.to_pandas_on_spark(index_col='index') # Uses the explicit index to avoid to create default index.


    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        teste_01_spark()

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
# python -m pip install --upgrade pyspark
# python -m pip install --upgrade pyspark[sql]
# python -m pip install --upgrade pyspark[pandas_on_spark] plotly
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
