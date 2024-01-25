import firebirdsql
import clickhouse_connect
import pandas as pd
from config import conf


def execute_sql_firebird(sql_type,sql_text, bd_type):
    conn = None
    try:
        # establishing the connection
        if bd_type == 'pub':
            conn = firebirdsql.connect(
                host=conf.pub_f_host,
                database=conf.pub_f_database,
                port=conf.pub_f_port,
                user=conf.pub_f_user,
                password=conf.pub_f_password
            )
        elif bd_type == 'pub_tar':
            conn = firebirdsql.connect(
                host=conf.pub_tar_f_host,
                database=conf.pub_tar_f_database,
                port=conf.pub_tar_f_port,
                user=conf.pub_tar_f_user,
                password=conf.pub_tar_f_password
            )
        else:
            conn = firebirdsql.connect(
                host=conf.f_host,
                database=conf.f_database,
                port=conf.f_port,
                user=conf.f_user,
                password=conf.f_password
            )

        # Creating a cursor object using the cursor() method
        cur = conn.cursor()
        # Retrieving data
        cur.execute(sql_text)
        if sql_type ==  'select':
            result = cur.fetchall()
            return result
        else:
            conn.commit()

    except Exception as error:
        print("Error while connecting to FireBird: execute_sql", error)
    finally:
        if conn:
            conn.close()

def execute_sql_clickhouse(sql_type, sql_text, par=None):
    try:
        client = clickhouse_connect.get_client(
                    host=conf.med_c_host,
                    port=conf.med_c_port,
                    username=conf.med_c_user,
                    password=conf.med_c_password)

        if sql_type == 'select':
            df = client.query_df(sql_text)
            return df
        else:
            client.command(sql_text, parameters=par)

    except Exception as error:
        print("Error while connecting to ClickHouse: execute_sql", error)


