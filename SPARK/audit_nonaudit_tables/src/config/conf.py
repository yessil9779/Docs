#[FireBird] source database
f_url = "jdbc:firebirdsql://ip:3050/E:\\broadview\\Database\\BVSREDMEDIA_TEST.FDB"
f_host = 'ip'
f_database = 'E:/broadview/Database/BVSREDMEDIA_TEST.FDB'
f_port = 3050
f_user = 'SYSDBA'
f_password = ''

#[FireBird PUBLICATION] table source (where we take table to process)
pub_f_host = 'ip'
pub_f_database = 'E:/broadview/Database/Publication/RM_OLAP_PUB_V2.FDB'
pub_f_port = 3050
pub_f_user = 'SYSDBA'
pub_f_password = ''

#[FireBird PUBLICATION TARGET] target database
pub_tar_f_url = "jdbc:firebirdsql://ip:3050/E:\\broadview\\Database\\Publication\\RM_OLAP_PUB_V2.FDB"
pub_tar_f_host = 'ip'
pub_tar_f_database = 'E:/broadview/Database/Publication/RM_OLAP_PUB_V2.FDB'
pub_tar_f_port = 3050
pub_tar_f_user = 'SYSDBA'
pub_tar_f_password = ''

#[Clickhouse PUBLICATION] clickhouse target database
pub_c_url = "jdbc:clickhouse://ip:18188/temp"
pub_c_host = 'ip'
pub_c_port = 18188
pub_c_user = 'default'
pub_c_password = ''
pub_c_schema =  'temp.'

# nonaudit_tables_list 
nonaudit_tables_list = ['VERSIONDATE','ASSETDATE','AMORTIZATIONHISTORY','SYSLOOKUP','TIMELINE_ATTRIBUTE','DATES','ASSET_LINK','TIMELINE_PBSBILLING','TIMELINE_PBS']


