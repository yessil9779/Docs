import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

# Удаление досрочного выхода на работу
try:
   df = db_conf.execute_sql(conf.del_early_exit_sql)

   for row in df.itertuples():

      logger.info("Tabel number: " + row.tab_number)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_tab_number(conf.num_employee,row.tab_number)
      logger.info("Find employee ItemID by tabel number: " + itemid_main)
   #----------------------------------------------------------
      if itemid_main == "": 
         update = db_conf.update_sql(req_res.update_text_n_pa(row.s_count, row.id))
         logger.info("Employee not found")

      else: 
         headers = get_xml_pa.get_header('UpdateObject')
         body = get_xml_pa.update_del_early_exit(conf.num_employee,itemid_main,row.employment)
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Employee card update responce" + response)
         
except:
    logger.info(sys.argv[0] + " ERROR")
    
