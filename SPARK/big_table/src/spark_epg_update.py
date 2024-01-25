from config import conf, db_conf, helper_func
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from datetime import datetime, timedelta

spark = SparkSession.builder\
    .appName("Pyspark")\
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "8g") \
    .getOrCreate()

# Function to read SQL query from a file
def read_sql_query(file_path, start_date, end_date):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_query = file.read()
    sql_query = sql_query.replace(':start_date', start_date).replace(':end_date', end_date)
    return sql_query

# Read SQL queries from files
sql_query_file_epg = "sql/epg.sql"
#------------------------------------------------------------------------------------------------- calculate interval
# Get the current date and time
current_date = datetime.now()

# Define the start and end dates
start_date = current_date - timedelta(days=15)
end_date = current_date

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
#------------------------------------------------------------------------------------------------- bigtable
sql_query_bigtable = f"SELECT * FROM {conf.bigtable} WHERE TLN_DATETIME between '{start_date_str}' and '{end_date_str}' and epg_playlist_view_id = ''"

df_bigtable_first = spark.read \
    .format("jdbc") \
    .option("url", conf.med_c_url) \
    .option("dbtable", f'({sql_query_bigtable}) AS subquery_alias') \
    .option("user", conf.med_c_user) \
    .option("password", conf.med_c_password) \
    .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
    .load()

# Getting a list of columns that do not start with "epg"
columns_to_keep = [col for col in df_bigtable_first.columns if not col.startswith("epg")]

# Creating a new Data Frame with the exception of the specified columns
df_bigtable = df_bigtable_first.select(columns_to_keep)
#------------------------------------------------------------------------------------------------- Epg
df_epg = spark.read \
    .format("jdbc") \
    .option("url", conf.mssql_url_olap) \
    .option("dbtable", f'({read_sql_query(sql_query_file_epg, start_date_str, end_date_str)}) AS subquery_alias') \
    .option("user", conf.mssql_user) \
    .option("password", conf.mssql_password) \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("trustServerCertificate", "true") \
    .load()

# Define the conditions for each join
join_condition_epg = (
        col("epg_playlist_view_beg_datetime").between(df_bigtable["TLN_DATETIME_BEG_EPG"], df_bigtable["TLN_DATETIME_END_EPG"]) &
        (col("epg_playlist_view_channel_id") == df_bigtable["CHANNEL_EPG_ID"])
)
#------------------------------------------------------------------------------------------------- bigtable update
df_bigtable_update = df_bigtable.join(df_epg, on=join_condition_epg, how="left")
#------------------------------------------------------------------------------------------------- UPDATE
# Iterate over rows in the PySpark DataFrame and update to clickhouse
for row in df_bigtable_update.rdd.collect():
    print(row['TLN_ID'])
    # 1. delete from clickhouse
    delete_query_c = f"ALTER TABLE {conf.bigtable} DELETE WHERE TLN_ID = {row['TLN_ID']}"
    db_conf.execute_sql_clickhouse('dml', delete_query_c)

    # 2. insert to clickhouse

        # Get INSERT form
    insert_columns = ','.join(df_bigtable_update.columns)
    insert_values = ','.join([helper_func.format_value(row[column]) for column in df_bigtable_update.columns])
    insert_query_c = f"INSERT INTO {conf.bigtable} ({insert_columns}) VALUES ({insert_values})"

        # Execute INSERT
    db_conf.execute_sql_clickhouse('dml', insert_query_c)
