import pymysql
from pymysql import converters
import pymysql.cursors


def get_connection_mysql(mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str) -> pymysql.connections.Connection: 
    converions = converters.conversions
    converions[pymysql.FIELD_TYPE.BIT] = lambda x: '0' if x == '\x00' else '1'
    connection = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database, cursorclass=pymysql.cursors.DictCursor, charset='utf8', conv=converions)
    return connection
