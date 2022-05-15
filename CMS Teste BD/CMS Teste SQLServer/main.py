import time
from dotenv import load_dotenv


def teste_pyodbc(host, user, password, database):
    try:

        print("pyodbc")

        import pyodbc

        # conn = pyodbc.connect("Driver={SQL Server};Server=DESKTOP-T2JV7P5;Database=PythonSQL;")
        conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password')
        # cnxn = pyodbc.connect(cnxn_str, autocommit=True)
        print("Conexão Bem Sucedida")

        cursor = conn.cursor()

        id = 3
        cliente = "Lira Python"
        produto = "Carro"
        data = "25/08/2021"
        preco = 5000
        quantidade = 1
        comando = f"""INSERT INTO Vendas(id_venda, cliente, produto, data_venda, preco, quantidade)VALUES({id}, '{cliente}', '{produto}', '{data}', {preco}, {quantidade})"""
        cursor.execute(comando)
        cursor.commit()

        # crsr = cnxn.cursor()
        # crsr.execute("PRINT 'Hello world!'")
        # print(crsr.messages)
        # cursor.execute("select a from tbl where b=? and c=?", (x, y))
        # cursor.execute("select a from tbl where b=? and c=?", x, y)

        # for row in cursor.execute("select user_id, user_name from users"):
        #     print(row.user_id, row.user_name)

        # row  = cursor.execute("select * from tmp").fetchone()
        # rows = cursor.execute("select * from tmp").fetchall()

        # count = cursor.execute("update users set last_logon=? where user_id=?", now, user_id).rowcount
        # count = cursor.execute("delete from users where user_id=1").rowcount
        # params = [ ('A', 1), ('B', 2) ]
        # cursor.executemany("insert into t(name, id) values (?, ?)", params)

        try:
            cnxn.autocommit = False
            params = [ ('A', 1), ('B', 2) ]
            cursor.executemany("insert into t(name, id) values (?, ?)", params)
        except pyodbc.DatabaseError as err:
            cnxn.rollback()
        else:
            cnxn.commit()
        finally:
            cnxn.autocommit = True

        cursor.execute("select user_name from users where user_id=?", userid)
        row = cursor.fetchone()
        if row:
            print(row.user_name)

        cursor.execute("select user_id, user_name from users where user_id < 100")
        rows = cursor.fetchall()
        for row in rows:
            print(row.user_id, row.user_name)

        # sql = "INSERT INTO product (item, price) VALUES (?, ?)"
        # params = [('bicycle', 499.99), ('ham', 17.95)]
        # crsr.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0), (pyodbc.SQL_DECIMAL, 18, 4)])  # specify that parameters are for NVARCHAR(50) and DECIMAL(18,4) columns
        # crsr.executemany(sql, params)

        for row in cursor.tables():
            print(row.table_name)

        # Does table 'x' exist?
        if cursor.tables(table='x').fetchone():
            print('yes it does')

        # with cnxn.cursor() as crsr:
        #     do_stuff

        # crsr = cnxn.cursor()
        # do_stuff
        # if not cnxn.autocommit:
        #     cnxn.commit()  

    except Exception as e:
        print(e)
        
        
def teste_pymssql(host, user, password, database):
    try:

        print("pymssql")

        import pymssql
        from pymssql import _mssql

        conn = pymssql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(as_dict=True)  # conn.cursor()

        cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        for row in cursor:
            print("ID=%d, Name=%s" % (row['id'], row['name']))

        cursor.executemany("INSERT INTO persons VALUES (%d, %s, %s)", [(1, 'John Smith', 'John Doe'), (2, 'Jane Doe', 'Joe Dog'), (3, 'Mike T.', 'Sarah H.')])
        conn.commit()
        
        cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        row = cursor.fetchone()
        while row:
            print("ID=%d, Name=%s" % (row[0], row[1]))
            row = cursor.fetchone()

        cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        for row in cursor:
            print('row = %r' % (row,))

        cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        for row in cursor:
            print("ID=%d, Name=%s" % (row['id'], row['name']))

        c1 = conn.cursor()
        c1.execute('SELECT * FROM persons')

        c2 = conn.cursor()
        c2.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')

        print( "all persons" )
        print( c1.fetchall() )  # shows result from c2 query!

        print( "John Doe" )
        print( c2.fetchall() )  # shows no results at all!

        conn.close()

        with pymssql.connect(host, user, password, "tempdb") as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
                for row in cursor:
                    print("ID=%d, Name=%s" % (row['id'], row['name']))

        # conn.bulk_copy("example", [(1, 2)] * 1000000)

        # examples of other query functions
        numemployees = conn.execute_scalar("SELECT COUNT(*) FROM employees")
        numemployees = conn.execute_scalar("SELECT COUNT(*) FROM employees WHERE name LIKE 'J%'")    # note that '%' is not a special character here
        employeedata = conn.execute_row("SELECT * FROM employees WHERE id=%d", 13)

    except Exception as e:
        print(e)


def main():
    try:

        start_time = time.time()

        host = "host"
        user = "root"
        password = "password"
        database = "database"

        teste_pyodbc(host=host, user=user, password=password, database=database)
        teste_pymssql(host=host, user=user, password=password, database=database)

        end_time = time.time()
        print(f"It took {end_time-start_time:.2f} seconds to compute")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade pyodbc
# python -m pip install --upgrade pymssql
# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py
# python3 main.py  
# pypy3 main.py
