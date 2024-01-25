import sys
import psycopg2
import pandas as pd
from config import conf
from config import log

logger = log.MyLogger(sys.argv[0])

def execute_sql(sql_text):
    conn = None
    try:
        #establishing the connection
        conn = psycopg2.connect(
            database="nifidb", 
            user=conf.nifi_username,
            password=conf.nifi_password,
            host='', 
            port= '')

        #Setting auto commit false
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        #Retrieving data
        cursor.execute(sql_text)

        #Fetching 1st row from the table
        result = cursor.fetchall();

        #Commit your changes in the database
        conn.commit()

        col_names = []
        for elt in cursor.description:
           col_names.append(elt[0])

        df = pd.DataFrame(result,columns=col_names)
        return df

    except (Exception, psycopg2.Error) as error:
        logger.info("Error while connecting to PostgreSQL: execute_sql", error)
    finally:
     if conn:
        cursor.close()
        conn.close()
        logger.info("PostgreSQL connection is closed: execute_sql")

def update_sql(sql_text):
    conn = None
    try:
        #establishing the connection
        conn = psycopg2.connect(
            database="nifidb", 
            user=conf.nifi_username,
            password=conf.nifi_password,
            host='', 
            port= '')

        #Setting auto commit false
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        #Retrieving data
        cursor.execute(sql_text)

        updated_rows = cursor.rowcount

        #Commit your changes in the database
        conn.commit()
        
        return updated_rows

    except (Exception, psycopg2.Error) as error:
        logger.info("Error while connecting to PostgreSQL: update_sql", error)
    finally:
     if conn:
        cursor.close()
        conn.close()
        logger.info("PostgreSQL connection is closed: update_sql")