import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Расторжение ГПХ
try:
   df = db_conf.execute_sql(conf.del_gph_sql)

   for row in df.itertuples():

      logger.info("IIN: " + row.iin)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_iin(row.iin)
      logger.info("Find employee ItemID by IIN: " + itemid_main)
   #----------------------------------------------------------
      if itemid_main == "": 
         update = db_conf.update_sql(req_res.update_text_n_pa(row.s_count, row.id))
         logger.info("Employee not found")

      else: 
         headers = get_xml_pa.get_header('UpdateObject')
         body = get_xml_pa.update_del_fact_gph(conf.num_employee,itemid_main)
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Employee card update responce" + response)
         
except:
    logger.info(sys.argv[0] + " ERROR")
    
