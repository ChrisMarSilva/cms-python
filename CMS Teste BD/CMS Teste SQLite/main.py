import time
import sqlite3
from dotenv import load_dotenv


def main():
    try:

        start_time = time.time()

        
        con = sqlite3.connect('example.db')
        # con = sqlite3.connect("file:template.db?mode=ro", uri=True)
        # con = sqlite3.connect("file:nosuchdb.db?mode=rw", uri=True)
        # con = db.from_url("sqlite3:///:memory:")
        # con = sqlite3.connect(":memory:")
        # con.isolation_level = None

        cur = con.cursor()
        cur.execute('''CREATE TABLE stocks(date text, trans text, symbol text, qty real, price real)''')
        cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
        con.commit()

        symbol = 'RHAT'
        cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

        for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
            print(row)

        cur.execute("create table lang (name, first_appeared)")
        cur.execute("insert into lang values (?, ?)", ("C", 1972))

        lang_list = [("Fortran", 1957),("Python", 1991),("Go", 2009),]
        cur.executemany("insert into lang values (?, ?)", lang_list)
        cur.execute("select * from lang where first_appeared=:year", {"year": 1972})
        print(cur.fetchall())

        con.execute(""" select * from pragma_compile_options where compile_options like 'THREADSAFE=%' """).fetchall()

        # con1 = sqlite3.connect("file:mem1?mode=memory&cache=shared", uri=True)
        # con2 = sqlite3.connect("file:mem1?mode=memory&cache=shared", uri=True)
        #con1.executescript("create table t(t); insert into t values(28);")
        #rows = con2.execute("select * from t").fetchall()

        cur.execute(""" SELECT * FROM clientes; """)
        for linha in cur.fetchall():
            print(linha)

        con.close()

        end_time = time.time()
        print(f"It took {end_time-start_time:.2f} seconds to compute")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade db-sqlite3
# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py

