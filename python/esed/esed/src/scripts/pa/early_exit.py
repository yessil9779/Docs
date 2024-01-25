import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

# Досрочный выход на работу
try:
   df = db_conf.execute_sql(conf.early_exit_sql)

   for row in df.itertuples():

      logger.info("Tabel number: " + row.tab_number)
   #---------------------------------------------------------- 
      headers = get_xml_pa.get_header('FindObjects')
      body = get_xml_pa.find_login_tabnumber(row.tab_number) 
      response = req_res.req(headers,body)

      itemid_main = req_res.check(response,'ItemID')
      Login = req_res.check(response,'FieldStringValue') 
      logger.info("Find the ItemID and Login of the employee by tabel number: " + itemid_main + ", "+ Login)
   #----------------------------------------------------------
      if itemid_main == "": 
         update = db_conf.update_sql(req_res.update_text_n_pa(row.s_count, row.id))
         logger.info("Employee not found")

      else: 
         if Login.startswith("SAP") or Login.startswith("MYERG"):
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.update_early_exit(itemid_main,row.employment,True)
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("Update employee card responce" + response)
         else:
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.update_early_exit(itemid_main,row.employment,False)
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("Update employee card responce" + response)
            
except:
    logger.info(sys.argv[0] + " ERROR")
    
