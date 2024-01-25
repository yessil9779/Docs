from config import conf,db_conf
from pyspark.sql import SparkSession

spark = SparkSession.builder\
    .appName("Pyspark")\
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

#------------------------------------------------------------------------------------------------- Mediahills
db_conf.execute_sql_clickhouse('dml', f"TRUNCATE TABLE {conf.med_c_table_name}")

# Set the connection properties
mssql_url_mediahills = conf.mssql_url_mediahills
mssql_properties_mediahills = {
    "user": conf.mssql_user,
    "password": conf.mssql_password,
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    "trustServerCertificate": "true"
}

# Get the list of tables
table_list = spark.read.jdbc(
    url=mssql_url_mediahills,
    table="(SELECT name FROM sys.views WHERE name LIKE 'report_tvchannels_%') AS subquery_alias",
    properties=mssql_properties_mediahills
)

# Iterate through the tables
for row in table_list.collect():
    table_name = row["name"]
    script = "(SELECT rp.channel_id as mediahills_report_tvchannels_channel_id, channel.name as mediahills_channel_view_name,city.name as mediahills_city_view_name,rp.dt as mediahills_report_tvchannels_dt,rp.audience_hm as mediahills_report_tvchannels_audience_hm,rp.reach_hm as mediahills_report_tvchannels_reach_hm,rp.reach as mediahills_report_tvchannels_reach,rp.share as mediahills_report_tvchannels_share,rp.tvr as mediahills_report_tvchannels_tvr FROM mediahills.{} rp LEFT JOIN mediahills.channel_view channel ON rp.channel_id = channel.id LEFT JOIN mediahills.city_view city ON rp.city_id = city.id WHERE rp.city_id = 1143) AS subquery_alias".format(table_name)
    # Read data
    try:
        table_data = spark.read.jdbc(
        url=mssql_url_mediahills,
        table="{}".format(script),
        properties=mssql_properties_mediahills
        )

        if table_data.count() > 0:
            # write to clickhouse
            try:
                table_data.write \
                    .format("jdbc") \
                    .option("url", conf.med_c_url) \
                    .option("dbtable", conf.med_c_table_name) \
                    .option("user", conf.med_c_user) \
                    .option("password", conf.med_c_password) \
                    .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
                    .option("createTableOptions",'ENGINE = MergeTree ORDER BY mediahills_report_tvchannels_channel_id') \
                    .mode("append") \
                    .save()
            except Exception as e:
                print(f"There is an error processing Clickhouse: {str(e)}")
        else:
            pass

    except Exception as e:
        print("Error reading table {}: {}".format(table_name, str(e)))

