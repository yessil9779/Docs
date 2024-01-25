#[postgresql]
nifi_username = ''
nifi_password = ''
#esed
esed_username = ''
esed_password = ''
url = ""
#log_folder
log_folder = r'/opt/nifi/scripts/esed/esed/src/logs/log.txt'
#cert_path
cert_path = r'/opt/nifi/scripts/esed/esed/src/cert/edms.pem'

num_part = 2536
num_employee = 1
num_company = 105
num_subdivision = 3
num_position = 2711
#--------------------------------------sql
#--pa
iin_mngr_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = 'P0001_SP' and begda <= now()::date and status_code <> '200' and s_count<=3'''
accept_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '01' and begda <= now()::date and status_code <> '200' and s_count<=3'''
change_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '0002' and status_code <> '200' and s_count<=3'''
early_exit_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '0402' and begda <= now()::date and status_code <> '200' and s_count<=3'''
gph_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '30' and status_code <> '200' and s_count<=3'''
parttime_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '23' and status_code <> '200' and s_count<=3'''
pregnant_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '0205' and begda <= now()::date and status_code <> '200' and s_count<=3'''
transfer_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '0298' and begda <= now()::date and status_code <> '200' and s_count<=3'''

del_early_exit_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = 'DEL_0402' and status_code <> '200' and s_count<=3'''
del_fact_td_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = 'D_10' and begda <= now()::date and status_code <> '200' and s_count<=3'''
del_gph_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '32' and begda <= now()::date and status_code <> '200' and s_count<=3'''
del_parttime_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = 'DEL_23' and status_code <> '200' and s_count<=3'''
del_pregnant_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = 'DEL_PREG' and status_code <> '200' and s_count<=3'''
del_td_sql = '''SELECT * from "HR_MI086"."agg_pa_table" where "event" = '10' and begda <= now()::date and status_code <> '200' and s_count<=3'''
#--om
del_position_sql = '''SELECT * from "HR_MI086"."agg_om_table" where "event" = 'DEL_S' and status_code <> '200' and s_count<=3'''
del_subdivision_sql = '''SELECT * from "HR_MI086"."agg_om_table" where "event" = 'DEL_O' and status_code <> '200' and s_count<=3'''
om_sql = '''SELECT * from "HR_MI086"."agg_om_table" where org_name <> '' and "event" in ('S','O') and status_code <> '200' and s_count<=3 order by rnk_o desc,event'''

