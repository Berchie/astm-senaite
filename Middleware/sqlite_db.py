import sqlite3
import os
from Middleware.senaite import show_message_box

db_dir = os.path.join(os.path.dirname(__file__), "..", "result_astm.db")


def create_db_table():
    try:
        # create connection and database
        con_sql = sqlite3.Connection(db_dir)

        # create cursor to execute SQL statement
        cur = con_sql.cursor()

        # SQL statement to CREATE TABLE
        sql_create_table = """
            CREATE TABLE IF NOT EXISTS transactions(
              datetime DATETIME,
              analyzer TEXT,
              sampleid TEXT,
              message BLOB,
              message_nx500 TEXT
            );
        """

        # execute sql statement
        cur.execute(sql_create_table)

        # commit the transaction
        con_sql.commit()

        cur.close()

        con_sql.close()

    except sqlite3.Error as e:
        print(f'An error occurred while creating database table: {e.sqlite_errorcode} - {e.sqlite_errorname}')
        show_message_box("Critical", "SQLite Error", f'Error occurred while creating database table: {(str(e))}')

    # finally:
    #    con.close()


def insert_record(t_date, t_analyzer, t_sampleid, t_message):
    # global con
    try:

        # create connection and database
        con = sqlite3.Connection(db_dir)

        # create cursor to execute SQL statement
        cur = con.cursor()

        # sql INSERT statement
        sql_insert = f'INSERT INTO transactions(datetime,analyzer, sampleid, message) VALUES(?,?,?,?);'

        cur.execute(sql_insert, (t_date, t_analyzer, t_sampleid, t_message))

        con.commit()

        cur.close()

        con.close()

    except sqlite3.Error as e:
        # print(f'An error occurred while inserting record into table: {e.sqlite_errorcode} {e}')
        show_message_box("Critical", "SQLite Error", f'Error occurred while inserting record into table: {str(e)}')
    # finally:
    #    con.close()


def insert_record_nx500(t_date, t_analyzer, t_sampleid, t_message):
    # global conn
    try:

        data_tuple = (t_date, t_analyzer, t_sampleid, t_message)

        # create connection and database
        conn = sqlite3.Connection(db_dir)

        # create cursor to execute SQL statement
        cursor = conn.cursor()

        # sql INSERT statement
        sql_insert_nx500 = 'INSERT INTO transactions(datetime,analyzer,sampleid, message_nx500) VALUES(?,?,?,?);'

        cursor.execute(sql_insert_nx500, data_tuple)

        conn.commit()

        cursor.close()

        conn.close()

    except sqlite3.OperationalError as e:
        show_message_box("Critical", "SQLite Error", f'Error occurred while inserting record into table: {str(e)}')
        # print(f'An error occurred while inserting record into table:Error code {e.sqlite_errorcode} - Error name:{e.sqlite_errorname} - \n e')
    # finally:
    #    if conn:
    #        conn.close()


if __name__ == '__main__':
    create_db_table()
