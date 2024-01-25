from config import conf, db_conf, helper_func
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col
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
sql_query_file_beeline = "sql/beeline.sql"
#------------------------------------------------------------------------------------------------- calculate interval
# Get the current date and time
current_date = datetime.now()

# Define the start and end dates
start_date = current_date - timedelta(days=15)
end_date = current_date

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
#------------------------------------------------------------------------------------------------- bigtable
sql_query_bigtable = f"SELECT * FROM {conf.bigtable} WHERE TLN_DATETIME between '{start_date_str}' and '{end_date_str}' and beeline_efir_view_channel_id = '0'"

df_bigtable_first = spark.read \
    .format("jdbc") \
    .option("url", conf.med_c_url) \
    .option("dbtable", f'({sql_query_bigtable}) AS subquery_alias') \
    .option("user", conf.med_c_user) \
    .option("password", conf.med_c_password) \
    .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
    .load()

# Getting a list of columns that do not start with "beeline"
columns_to_keep = [col for col in df_bigtable_first.columns if not col.startswith("beeline")]

# Creating a new Data Frame with the exception of the specified columns
df_bigtable = df_bigtable_first.select(columns_to_keep)
#------------------------------------------------------------------------------------------------- Beeline
df_beeline = spark.read \
        .format("jdbc") \
        .option("url", conf.mssql_url_olap) \
        .option("dbtable", f'({read_sql_query(sql_query_file_beeline, start_date_str, end_date_str)}) AS subquery_alias') \
        .option("user", conf.mssql_user) \
        .option("password", conf.mssql_password) \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .option("trustServerCertificate", "true") \
        .load()

# join_condition
join_condition_beeline = (
        (col("beeline_efir_view_efir_beg_date") >= df_bigtable["TLN_DATETIME"]) &
        (col("beeline_efir_view_efir_end_date") <= df_bigtable["TLN_DATETIME_END"]) &
        (col("beeline_channel_view_bv_id") == df_bigtable["TLN_CHA_ID"])
    )

group_by_columns_df_bigtable = [col_name for col_name in df_bigtable.columns]

# Add the additional columns to the grouping
additional_columns_beeline = ["beeline_efir_view_channel_id","beeline_efir_view_efir_date"]

group_by_columns_df_bigtable.extend(additional_columns_beeline)
#------------------------------------------------------------------------------------------------- bigtable update
df_bigtable_update = df_bigtable\
            .join(df_beeline, on=join_condition_beeline, how="left") \
            .groupBy(group_by_columns_df_bigtable) \
            .agg(
                avg("beeline_efir_view_time_view").alias("beeline_efir_view_time_view"),
                avg("beeline_efir_view_scope").alias("beeline_efir_view_scope"),
                avg("beeline_efir_view_cnt_connect").alias("beeline_efir_view_cnt_connect"),
                avg("beeline_efir_view_cnt_disconnect").alias("beeline_efir_view_cnt_disconnect"),
                avg("beeline_efir_view_time_view_avg").alias("beeline_efir_view_time_view_avg"),
                avg("beeline_efir_view_time_view_avg_connect").alias("beeline_efir_view_time_view_avg_connect"),
                avg("beeline_efir_view_scope_avg").alias("beeline_efir_view_scope_avg"),
                avg("beeline_efir_view_tvr").alias("beeline_efir_view_tvr"),
                avg("beeline_efir_view_cnt").alias("beeline_efir_view_cnt"),
                avg("beeline_efir_view_tvr_max").alias("beeline_efir_view_tvr_max"),
                avg("beeline_efir_view_cnt_max").alias("beeline_efir_view_cnt_max")
                ) \
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
