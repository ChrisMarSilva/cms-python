from loguru import logger
import time
import sqlite3
import pandas as pd
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        logger.info(f"Carregando DataFrame do CSV...")
        df = pd.read_csv(filepath_or_buffer='sales_data_simplified.csv', sep=',', index_col=0)
        # logger.info(df.head(10))

        logger.info(f"Conectando...")
        with sqlite3.connect(database='example.db') as con:
            # logger.info(f"Inserindo...")
            # df.to_sql(name='sales', con=con, if_exists="replace")  # if_exists : {'fail', 'replace', 'append'}
            cur = con.cursor()
            #cur.execute("SELECT * FROM sales")
            # logger.info(cur.fetchall())
            # for linha in cur.fetchall():
            #     logger.info(linha)
            logger.info(f"Consultando...")
            cur.execute("SELECT count(1) FROM sales")
            logger.info(cur.fetchone()) # 185951 csv # 185950 bd
            cur.close()

        logger.info(f"Carregando DataFrame do BD...")
        df_read = pd.read_sql(sql='SELECT * FROM sales', con=con)
        # logger.info(df_read.head(10))

        logger.info(f"Carregando DataFrame do BD com Where...")
        sql = """   SELECT "id", "product", "quantity", "price", "quantity" * "price" as "total"
                    FROM sales 
                    WHERE "product" = "USB-C Charging Cable" 
            """
        df_read = pd.read_sql(sql=sql, con=con, index_col="id")
        # logger.info(df_read.head(10))

        logger.info(f"Conectando...")
        with sqlite3.connect(database='example.db') as con:
            # logger.info(f"Inserindo...")
            # df_read.to_sql(name='sales', con=con, if_exists="replace") 
            sql = 'SELECT * FROM sales'
            df_read2 = pd.read_sql(sql=sql, con=con)
            logger.info(df_read2.head(10))

        con.close()

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade db-sqlite3
# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py
