from config import conf, db_conf, helper_func
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col
from datetime import datetime, timedelta

spark = SparkSession.builder\
    .appName("Pyspark")\
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "8g") \
    .getOrCreate()

#------------------------------------------------------------------------------------------------- calculate interval
# Get the current date and time
current_date = datetime.now()

# Define the start and end dates
start_date = current_date - timedelta(days=15)
end_date = current_date

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
#------------------------------------------------------------------------------------------------- bigtable
sql_query_bigtable = f"SELECT * FROM {conf.bigtable} WHERE TLN_DATETIME between '{start_date_str}' and '{end_date_str}' and mediahills_channel_view_name = ''"

df_bigtable_first = spark.read \
    .format("jdbc") \
    .option("url", conf.med_c_url) \
    .option("dbtable", f'({sql_query_bigtable}) AS subquery_alias') \
    .option("user", conf.med_c_user) \
    .option("password", conf.med_c_password) \
    .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
    .load()

# Getting a list of columns that do not start with "epg"
columns_to_keep = [col for col in df_bigtable_first.columns if not col.startswith("mediahills")]

# Creating a new Data Frame with the exception of the specified columns
df_bigtable = df_bigtable_first.select(columns_to_keep)
#------------------------------------------------------------------------------------------------- Epg
sql_query_mediahills = f"SELECT * FROM {conf.med_c_table_name} WHERE mediahills_report_tvchannels_dt between '{start_date_str}' and '{end_date_str}'"

df_mediahills = spark.read \
    .format("jdbc") \
    .option("url", conf.med_c_url) \
    .option("dbtable", f'({sql_query_mediahills}) AS subquery_alias') \
    .option("user", conf.med_c_user) \
    .option("password", conf.med_c_password) \
    .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
    .load()

join_condition_mediahills = (
        col("mediahills_report_tvchannels_dt").between(df_bigtable["TLN_DATETIME"], df_bigtable["TLN_DATETIME_END"]) &
        (col("mediahills_report_tvchannels_channel_id") == df_bigtable["CHANNEL_MEDIAHILLS_ID"])
)

group_by_columns_df_bigtable = [col_name for col_name in df_bigtable.columns]

# Add the additional columns to the grouping
additional_columns_mediahills = [
    "mediahills_channel_view_name",
    "mediahills_city_view_name"
]

group_by_columns_df_bigtable.extend(additional_columns_mediahills)
#------------------------------------------------------------------------------------------------- bigtable update
df_bigtable_update = df_bigtable.join(df_mediahills, on=join_condition_mediahills, how="left") \
            .groupBy(group_by_columns_df_bigtable) \
            .agg(
                avg("mediahills_report_tvchannels_audience_hm").alias("mediahills_report_tvchannels_audience_hm"),
                avg("mediahills_report_tvchannels_reach_hm").alias("mediahills_report_tvchannels_reach_hm"),
                avg("mediahills_report_tvchannels_reach").alias("mediahills_report_tvchannels_reach"),
                avg("mediahills_report_tvchannels_share").alias("mediahills_report_tvchannels_share"),
                avg("mediahills_report_tvchannels_tvr").alias("mediahills_report_tvchannels_tvr")
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
