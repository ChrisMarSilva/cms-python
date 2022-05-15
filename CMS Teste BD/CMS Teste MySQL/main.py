from loguru import logger
import time
import datetime as dt
from dotenv import load_dotenv


def teste_mysql_connector(host, user, password, database):
    try:

        print("mysql.connector")

        import mysql.connector
        from mysql.connector import errorcode

        cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
        # config = {'user': user, 'password': password, 'host': host, 'database': database, 'raise_on_warnings': True, 'use_pure': False}
        # cnx = mysql.connector.connect(**config)
        try:

            cursor = cnx.cursor()
            try:

                print("DATABASES")
                cursor.execute("SHOW DATABASES")
                for x in cursor:
                    print(x)

                print("TABLES")
                cursor.execute("SHOW TABLES")
                for x in cursor:
                    print(x)

                # add_employee = ("INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)")
                # add_salary = ("INSERT INTO salaries (emp_no, salary, from_date, to_date) VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

                # tomorrow = dt.datetime.now().date() + dt.timedelta(days=1)

                # # Insert new employee
                # data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', dt.date(1977, 6, 14))
                # cursor.execute(add_employee, data_employee)
                # emp_no = cursor.lastrowid   

                # # Insert salary information
                # data_salary = {'emp_no': emp_no, 'salary': 50000, 'from_date': tomorrow, 'to_date': dt.date(9999, 1, 1) }
                # cursor.execute(add_salary, data_salary)
                
                # cnx.commit() # Make sure data is committed to the database

                # query = ("SELECT first_name, last_name, hire_date FROM employees WHERE hire_date BETWEEN %s AND %s")
                # hire_start = dt.datetime.date(1999, 1, 1)
                # hire_end = dt.datetime.date(1999, 12, 31)
                # cursor.execute(query, (hire_start, hire_end))
                # for (first_name, last_name, hire_date) in cursor:
                #     print("{}, {} was hired on {:%d %b %Y}".format(last_name, first_name, hire_date))

                # sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
                # val = ("John", "Highway 21")
                # cursor.execute(sql, val)
                # cnx.commit()
                # print("1 record inserted, ID:", cursor.lastrowid)

                # sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
                # val = [('Peter', 'Lowstreet 4'),('Amy', 'Apple st 652'),('Hannah', 'Mountain 21'),('Michael', 'Valley 345'),('Sandy', 'Ocean blvd 2'),('Betty', 'Green Grass 1'),('Richard', 'Sky st 331'),('Susan', 'One way 98'),('Vicky', 'Yellow Garden 2'),('Ben', 'Park Lane 38'),('William', 'Central st 954'),('Chuck', 'Main Road 989'),('Viola', 'Sideway 1633')]
                # cursor.executemany(sql, val)
                # cnx.commit()

                # mycursor.execute("SELECT * FROM customers")
                # myresult = mycursor.fetchall()
                # for x in myresult:
                #     print(x)

                # mycursor.execute("SELECT * FROM customers")
                # myresult = mycursor.fetchone()
                # print(myresult)

                # sql = "SELECT * FROM customers WHERE address = %s"
                # adr = ("Yellow Garden 2", )
                # mycursor.execute(sql, adr)

            finally:
                cursor.close()
                
            # with connection.cursor() as cursor:
            #     cursor.execute("create_db_query")
            # cursor.execute(create_movies_table_query)
            # cursor.execute(create_reviewers_table_query)
            # cursor.execute(create_ratings_table_query)
            #  connection.commit()

            #  show_table_query = "DESCRIBE movies"
            #  with connection.cursor() as cursor:
            #      cursor.execute(show_table_query)
            #      # Fetch rows from last executed query
            #      result = cursor.fetchall()
            #      for row in result:
            #          print(row)

        finally:
            cnx.close()

    except mysql.connector.Error as err:
        # if err.errno == errorcode.ER_BAD_DB_ERROR:
        #     print("Database {} created successfully.".format(DB_NAME))
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    except Exception as e:
        print(e)


def teste_pymysql(host, user, password, database):
    try:

        print("pymysql")
            
        import pymysql
        import pymysql.cursors

        connection = pymysql.connect(host=host, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)

        with connection:
            #with connection.cursor() as cursor:
                # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
            #connection.commit()
            # with connection.cursor() as cursor:
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
            with connection.cursor() as cursor:
                sql = "SHOW DATABASES"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)

    except Exception as e:
        print(e)



def teste_pymysql_insert_proventos(host, user, password, database):
    try:

        print("pymysql")
            
        import pymysql
        import pymysql.cursors

        connection = pymysql.connect(host=host, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                sql = " INSERT INTO TBFII_FUNDOIMOB_PROVENTO ( IDFUNDO, TIPO, CATEGORIA, CODISIN, DATAAPROV, DATACOM, DATAEX, DATAPAGTO, VLRPRECO, SITUACAO ) SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS( SELECT 1 FROM TBFII_FUNDOIMOB_PROVENTO PRV WHERE PRV.IDFUNDO = %s AND PRV.TIPO = %s AND PRV.CODISIN = %s AND PRV.DATAAPROV = %s AND PRV.DATAEX = %s AND PRV.DATAPAGTO = %s AND PRV.VLRPRECO =%s )  "
                val = [
                    # ('IDFUNDO': 813, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRBLURCTF005', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '1.03000000000', 'SITUACAO': 'A', 'IDFUNDO2': 813, 'TIPO2': 'R', 'CODISIN2': 'BRBLURCTF005', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '1.03000000000'), 
                    # ('IDFUNDO': 755, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRIBCRCTF009', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '1.22000000000', 'SITUACAO': 'A', 'IDFUNDO2': 755, 'TIPO2': 'R', 'CODISIN2': 'BRIBCRCTF009', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '1.22000000000'), 
                    # ('IDFUNDO': 622, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRIBFFCTF007', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '0.50000000000', 'SITUACAO': 'A', 'IDFUNDO2': 622, 'TIPO2': 'R', 'CODISIN2': 'BRIBFFCTF007', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '0.50000000000'), 
                    # ('IDFUNDO': 781, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRGAMECTF002', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220520', 'VLRPRECO': '0.14000000000', 'SITUACAO': 'A', 'IDFUNDO2': 781, 'TIPO2': 'R', 'CODISIN2': 'BRGAMECTF002', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220520', 'VLRPRECO2': '0.14000000000'), 
                    # ('IDFUNDO': 486, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRIRDMCTF004', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '1.26096202700', 'SITUACAO': 'A', 'IDFUNDO2': 486, 'TIPO2': 'R', 'CODISIN2': 'BRIRDMCTF004', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '1.26096202700'), 
                    # ('IDFUNDO': 776, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRIRIMCTF003', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '1.51057933800', 'SITUACAO': 'A', 'IDFUNDO2': 776, 'TIPO2': 'R', 'CODISIN2': 'BRIRIMCTF003', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '1.51057933800'), 
                    # ('IDFUNDO': 641, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRRBRMCTF009', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '7415.14684608', 'SITUACAO': 'A', 'IDFUNDO2': 641, 'TIPO2': 'R', 'CODISIN2': 'BRRBRMCTF009', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '7415.14684608'), 
                    # ('IDFUNDO': 605, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRRBRYCTF004', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '1.25000000000', 'SITUACAO': 'A', 'IDFUNDO2': 605, 'TIPO2': 'R', 'CODISIN2': 'BRRBRYCTF004', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '1.25000000000'), 
                    # ('IDFUNDO': 535, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRRBRFCTF003', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '0.60000000000', 'SITUACAO': 'A', 'IDFUNDO2': 535, 'TIPO2': 'R', 'CODISIN2': 'BRRBRFCTF003', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '0.60000000000'), 
                    # ('IDFUNDO': 537, 'TIPO': 'R', 'CATEGORIA': 'CI', 'CODISIN': 'BRRBRRCTF008', 'DATAAPROV': '20220510', 'DATACOM': '', 'DATAEX': '20220511', 'DATAPAGTO': '20220517', 'VLRPRECO': '1.20000000000', 'SITUACAO': 'A', 'IDFUNDO2': 537, 'TIPO2': 'R', 'CODISIN2': 'BRRBRRCTF008', 'DATAAPROV2': '20220510', 'DATAEX2': '20220511', 'DATAPAGTO2': '20220517', 'VLRPRECO2': '1.20000000000'),
                    (813, 'R', 'CI', 'BRBLURCTF005', '20220510', '', '20220511', '20220517', '1.03000000000', 'A', 813, 'R', 'BRBLURCTF005', '20220510', '20220511', '20220517', '1.03000000000'), 
                    (755, 'R', 'CI', 'BRIBCRCTF009', '20220510', '', '20220511', '20220517', '1.22000000000', 'A', 755, 'R', 'BRIBCRCTF009', '20220510', '20220511', '20220517', '1.22000000000'), 
                    (622, 'R', 'CI', 'BRIBFFCTF007', '20220510', '', '20220511', '20220517', '0.50000000000', 'A', 622, 'R', 'BRIBFFCTF007', '20220510', '20220511', '20220517', '0.50000000000'), 
                    (781, 'R', 'CI', 'BRGAMECTF002', '20220510', '', '20220511', '20220520', '0.14000000000', 'A', 781, 'R', 'BRGAMECTF002', '20220510', '20220511', '20220520', '0.14000000000'), 
                    (486, 'R', 'CI', 'BRIRDMCTF004', '20220510', '', '20220511', '20220517', '1.26096202700', 'A', 486, 'R', 'BRIRDMCTF004', '20220510', '20220511', '20220517', '1.26096202700'), 
                    (776, 'R', 'CI', 'BRIRIMCTF003', '20220510', '', '20220511', '20220517', '1.51057933800', 'A', 776, 'R', 'BRIRIMCTF003', '20220510', '20220511', '20220517', '1.51057933800'), 
                    (641, 'R', 'CI', 'BRRBRMCTF009', '20220510', '', '20220511', '20220517', '7415.14684608', 'A', 641, 'R', 'BRRBRMCTF009', '20220510', '20220511', '20220517', '7415.14684608'), 
                    (605, 'R', 'CI', 'BRRBRYCTF004', '20220510', '', '20220511', '20220517', '1.25000000000', 'A', 605, 'R', 'BRRBRYCTF004', '20220510', '20220511', '20220517', '1.25000000000'), 
                    (535, 'R', 'CI', 'BRRBRFCTF003', '20220510', '', '20220511', '20220517', '0.60000000000', 'A', 535, 'R', 'BRRBRFCTF003', '20220510', '20220511', '20220517', '0.60000000000'), 
                    (537, 'R', 'CI', 'BRRBRRCTF008', '20220510', '', '20220511', '20220517', '1.20000000000', 'A', 537, 'R', 'BRRBRRCTF008', '20220510', '20220511', '20220517', '1.20000000000'),
                ]
                # cursor.execute(sql, val)
                cursor.executemany(sql, val)
                connection.commit()

    except Exception as e:
        print(e)

def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        host     = "localhost"  # '127.0.0.1'
        port     = "3306"
        database = "database"
        user     = "root"
        password = "password"

        # teste_mysql_connector(host=host, user=user, password=password, database=database)
        # teste_pymysql(host=host, user=user, password=password, database=database)

        teste_pymysql_insert_proventos(host=host, user=user, password=password, database=database)

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
# python -m pip install --upgrade mysql-connector-python
# python -m pip install --upgrade PyMySQL
# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py
