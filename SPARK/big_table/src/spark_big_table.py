from config import conf, db_conf
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, expr
from datetime import datetime, timedelta
import calendar

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
sql_query_file_f = "sql/vw_timeline_program.sql"
sql_query_file_epg = "sql/epg.sql"
sql_query_file_beeline = "sql/beeline.sql"

db_conf.execute_sql_clickhouse('dml', f"TRUNCATE TABLE {conf.bigtable}")
#------------------------------------------------------------------------------------------------- calculate interval
# Define the start and end dates
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 12, 31)

while start_date <= end_date:
    # Find the last day of the current month
    _, last_day_of_month = calendar.monthrange(start_date.year, start_date.month)
    # Calculate the end date for the current month
    end_date_month = datetime(start_date.year, start_date.month, last_day_of_month)
    # Ensure the end date does not exceed the global end_date
    current_end_date = min(end_date, end_date_month)
    # Convert the current start_date and end_date to string format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = current_end_date.strftime('%Y-%m-%d')
#------------------------------------------------------------------------------------------------- VW_TIMELINE_PROGRAM
    df_f = spark.read \
        .format("jdbc") \
        .option("url", conf.pub_f_url) \
        .option("dbtable", f'({read_sql_query(sql_query_file_f, start_date_str, end_date_str)}) AS subquery_alias') \
        .option("user", conf.pub_f_user) \
        .option("password", conf.pub_f_password) \
        .option("driver", "org.firebirdsql.jdbc.FBDriver") \
        .load()
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
        col("epg_playlist_view_beg_datetime").between(df_f["TLN_DATETIME_BEG_EPG"], df_f["TLN_DATETIME_END_EPG"]) &
        (col("epg_playlist_view_channel_id") == df_f["CHANNEL_EPG_ID"])
    )
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

    #Условие соединения
    join_condition_beeline = (
        (col("beeline_efir_view_efir_beg_date") >= df_f["TLN_DATETIME"]) &
        (col("beeline_efir_view_efir_end_date") <= df_f["TLN_DATETIME_END"]) &
        (col("beeline_channel_view_bv_id") == df_f["TLN_CHA_ID"])
    )

    group_by_columns_df_f = [col_name for col_name in df_f.columns]
    # Add the additional columns to the grouping
    additional_columns_beeline = [
        "beeline_efir_view_channel_id",
        "beeline_efir_view_efir_date"
    ]

    group_by_columns_df_f.extend(additional_columns_beeline)
#------------------------------------------------------------------------------------------------- Mediahills
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
        col("mediahills_report_tvchannels_dt").between(df_f["TLN_DATETIME"], df_f["TLN_DATETIME_END"]) &
        (col("mediahills_report_tvchannels_channel_id") == df_f["CHANNEL_MEDIAHILLS_ID"])
    )

    # Add the additional columns to the grouping
    additional_columns_mediahills = [
        "mediahills_channel_view_name",
        "mediahills_city_view_name"
    ]

    group_by_columns_df_f.extend(additional_columns_mediahills)
#------------------------------------------------------------------------------------------------- BIGTABLE
    df_bigtable = df_f\
            .join(df_beeline, on=join_condition_beeline, how="left") \
            .join(df_mediahills, on=join_condition_mediahills, how="left") \
            .groupBy(group_by_columns_df_f) \
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
                avg("beeline_efir_view_cnt_max").alias("beeline_efir_view_cnt_max"),
                avg("mediahills_report_tvchannels_audience_hm").alias("mediahills_report_tvchannels_audience_hm"),
                avg("mediahills_report_tvchannels_reach_hm").alias("mediahills_report_tvchannels_reach_hm"),
                avg("mediahills_report_tvchannels_reach").alias("mediahills_report_tvchannels_reach"),
                avg("mediahills_report_tvchannels_share").alias("mediahills_report_tvchannels_share"),
                avg("mediahills_report_tvchannels_tvr").alias("mediahills_report_tvchannels_tvr")
                ) \
            .join(df_epg, on=join_condition_epg, how="left")

    primary_key = 'TLN_ID'

    df_bigtable.write \
               .format("jdbc") \
               .option("url", conf.med_c_url) \
               .option("dbtable", conf.bigtable) \
               .option("user", conf.med_c_user) \
               .option("password", conf.med_c_password) \
               .option("createTableOptions", 'ENGINE = MergeTree PRIMARY KEY ' + primary_key + ' ORDER BY ' + primary_key) \
               .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
               .mode("append") \
               .save()

    # Increment the start_date for the next iteration
    start_date = end_date_month + timedelta(days=1)