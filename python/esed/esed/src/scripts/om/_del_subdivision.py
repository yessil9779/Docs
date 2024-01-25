import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_om,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Удаление наименовании подразделении
try:
   df = db_conf.execute_sql(conf.del_subdivision_sql)

   for row in df.itertuples():

      logger.info("Sap_id: " + row.sap_id)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_subdivision(row.sap_id)
      logger.info("Find subdivision ItemID: " + itemid_main)
   #---------------------------------------------------------- 
      
      if itemid_main == "": 
         update = db_conf.update_sql(req_res.update_text_n_om(row.id))
         logger.info("Subdivision not found!")

      else: 
         headers = get_xml_om.get_header('UpdateObject')
         body = get_xml_om.del_object(conf.num_subdivision,itemid_main)
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_om(response,row.s_count,row.id))
         logger.info("Delete subdivision responce: " + response)
         
except:
    logger.info(sys.argv[0] + " ERROR")
    
