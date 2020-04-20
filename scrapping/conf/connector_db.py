from sqlite3 import OperationalError

import mysql.connector

import scrapping.conf.properties as conf


class ConnectorDB:
    def __init__(self):
        """
        init database
        """
        my_db = mysql.connector.connect(
            host=conf.HOST,
            user=conf.USERNAME,
            passwd=conf.PASSWORD,
            auth_plugin=conf.AUTH_PLUGIN
        )
        self.db = my_db

    def set_db(self):
        """
        use scrapping database
        """
        self.db.database = 'scrapping'

    def creation_db_script(self):
        """
        run creation script to create database and tables
        """
        with open(conf.SCRIPT_CREATION, 'r') as fd:
            sql_file = fd.read()

        sql_to_execute = sql_file.split(';')
        c = self.db.cursor()
        # Execute every command from the input file
        for command in sql_to_execute:
            try:
                c.execute(command)
            except OperationalError as msg:
                print("Command skipped: ", msg)
        c.close()
        self.db.commit()
        self.db.close()

    def get_db_conn(self):
        """
        configure DB connection
        :return:  db connector
        """
        if not self.db.database:
            self.set_db()
        return self.db

    def __del__(self):
        """
        close connection to db
        """
        self.db.close()


def main():
    """This file can be used as a standalone
     to create the database structure"""
    conn = ConnectorDB()
    conn.creation_db_script()
    conn.__del__()


if __name__ == '__main__':
    main()
