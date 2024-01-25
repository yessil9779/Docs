import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Изменение iin_mngr при смене руководителя
try:
   df = db_conf.execute_sql(conf.iin_mngr_sql)

   for row in df.itertuples():

      logger.info("Tabel number: " + row.tab_number)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_tab_number(conf.num_employee,row.tab_number)
      logger.info("Find employee ItemID by tab number: " + itemid_main)

      itemid_mngr = req_res.ifnull(req_res.get_emp_by_iin(row.iin_mngr))
      logger.info("Find manager ItemID by iin: " + itemid_mngr)
   #---------------------------------------------------------- 
      
      if itemid_main == "":
         update = db_conf.update_sql(req_res.update_text_n_pa(row.s_count, row.id))
         logger.info("Employee not found")

      else: 
         headers = get_xml_pa.get_header('UpdateObject')
         body = get_xml_pa.update_iin_mngr(conf.num_employee,
                                          itemid_main,
                                          itemid_mngr
                                       )
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Update employee responce: " + response)
            
except:
   logger.info(sys.argv[0] + " ERROR")
    
