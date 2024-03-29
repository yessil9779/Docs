from config import db_conf, conf, helper_func
from pyspark.sql import SparkSession
from airflow.models import Variable


# Get max_saa_id
max_saa_id = db_conf.execute_sql_firebird('select', 'SELECT max(saa_id) FROM SYS_A$AUDIT', 'f')
Variable.set("max_saa_id", max_saa_id[0][0])

# Get all table names from pub_db
all_tables_list = db_conf.execute_sql_firebird('select', 'SELECT PUB_TABLENAME,TAB_ID FROM VW_SYS_A$TABLE_INIT', 'pub')

spark = SparkSession \
            .builder \
            .appName("Pyspark") \
            .getOrCreate()

# Get every table
for x in all_tables_list:
  table_name = x[0]
  print(table_name)

  df = spark.read \
    .format("jdbc") \
    .option("url", conf.f_url) \
    .option("dbtable", table_name) \
    .option("user", conf.f_user) \
    .option("password", conf.f_password) \
    .option("driver", "org.firebirdsql.jdbc.FBDriver") \
    .load()

  primary_key = df.columns[0]

  # columns_to_exclude
  calc_columns = db_conf.execute_sql_firebird('select', helper_func.get_calc_columns(table_name), 'f')
  columns_to_exclude = [col[0] for col in calc_columns]
  columns_to_include = [col for col in df.columns if col not in columns_to_exclude]
  df_filtered = df.select(columns_to_include)

  # DELETE all from clikchouse table
  db_conf.execute_sql_clickhouse('dml', f"TRUNCATE TABLE {conf.pub_c_schema + table_name}")

  # write to clickhouse
  try:
    df_filtered.write \
        .format("jdbc") \
        .option("url", conf.pub_c_url) \
        .option("dbtable", conf.pub_c_schema + table_name) \
        .option("user", conf.pub_c_user) \
        .option("password", conf.pub_c_password) \
        .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
        .option("createTableOptions", 'ENGINE = MergeTree PRIMARY KEY ' + primary_key + ' ORDER BY ' + primary_key) \
        .mode("append") \
        .save()
  except Exception as e:
    print(f"There is an error processing Clickhouse: {str(e)}")

  # delete all from firebird publication
  db_conf.execute_sql_firebird('dml', f"DELETE FROM {table_name}", 'pub_tar')

  # write to firebird publication target
  try:
    df_filtered.write \
      .format("jdbc") \
      .option("url", conf.pub_tar_f_url) \
      .option("dbtable", table_name) \
      .option("user", conf.pub_tar_f_user) \
      .option("password", conf.pub_tar_f_password) \
      .option("driver", "org.firebirdsql.jdbc.FBDriver") \
      .mode("append") \
      .save()
  except Exception as e:
    print(f"There is an error writing to Firebird: {str(e)}")


