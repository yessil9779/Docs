#[FireBird]
f_url = "jdbc:firebirdsql://ip:3050/D:\\broadview\\Database\\BVSREDMEDIA_TEST.FDB"
f_host = 'ip'
f_database = 'D:/broadview/Database/BVSREDMEDIA_TEST.FDB'
f_port = 3050
f_user = 'SYSDBA'
f_password = ''

#[FireBird PUBLICATION]
pub_f_url = "jdbc:firebirdsql://ip:3050/D:\\broadview\\Database\\Publication\\RM_OLAP_PUB_NEW.FDB"
pub_f_host = 'ip'
pub_f_database = 'D:/broadview/Database/Publication/RM_OLAP_PUB_NEW.FDB'
pub_f_port = 3050
pub_f_user = 'SYSDBA'
pub_f_password = ''


#[FireBird PUBLICATION TARGET]
pub_tar_f_url = "jdbc:firebirdsql://ip:3050/E:\\broadview\\Database\\Publication\\RM_OLAP_PUB_NEW.FDB"
pub_tar_f_host = 'ip'
pub_tar_f_database = 'E:/broadview/Database/Publication/RM_OLAP_PUB_NEW.FDB'
pub_tar_f_port = 3050
pub_tar_f_user = 'SYSDBA'
pub_tar_f_password = ''

#[Clickhouse PUBLICATION]
pub_c_url = "jdbc:clickhouse://ip:18188/default"
pub_c_host = 'ip'
pub_c_port = 18188
pub_c_user = 'default'
pub_c_password = ''
pub_c_schema =  'default.'

#[MSSQL]
mssql_url_olap = "jdbc:sqlserver://ip:1433;databaseName=olap"
mssql_url_mediahills = "jdbc:sqlserver://ip:1433;databaseName=mediahills"
mssql_host = 'ip'
mssql_port = 1433
mssql_user = 'olap'
mssql_password = ''
mssql_schema =  'temp.'

#[FOR UNION MEDIAHILLS TABLE]
med_c_url = "jdbc:clickhouse://ip:8123/default"
med_c_host = 'ip'
med_c_port = 8123
med_c_user = 'default'
med_c_password = ''
med_c_table_name = "default.mediahills_big_table"

#Bigtable
bigtable = 'default.bigtable'
#bigtable = 'default.bigtable_c'
#bigtable = 'default.bigtable_cc'