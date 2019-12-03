import mysql.connector


def get_db_conn():
    """
    configure DB connection
    :return:  db connector
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="username",
        passwd="password",
        database="scrapping",
        auth_plugin='mysql_native_password'
    )
    return mydb
