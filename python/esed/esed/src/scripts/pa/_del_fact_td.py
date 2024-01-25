import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Удаление расторжения ТД:
try:
   df = db_conf.execute_sql(conf.del_fact_td_sql)

   for row in df.itertuples():
       
      logger.info("Tabel number: " + row.tab_number)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_tab_number(conf.num_employee,row.tab_number)
      logger.info("Find employee ItemID by tabel number: " + itemid_main)
   #---------------------------------------------------------- 
      if itemid_main == "":  
         headers = get_xml_pa.get_header('FindObjects')
         body = get_xml_pa.find_objects_fired(conf.num_part,"[Табельный номер] = N'"+row.tab_number+"' AND [Deleted] = 0") 
         response = req_res.req(headers,body)
         logger.info("Find in the list of combining response: " + response)
         #----------------------------------------
         ItemID = req_res.check(response,'ItemID')
         logger.info("Find ItemID in the combination list: " + ItemID)

         if ItemID != "":
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.fact_del(conf.num_part,ItemID,"False")
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("Update in combination list responce : " + response)
         else:
            update = db_conf.update_sql(req_res.update_text_n_pa(row.s_count, row.id))
            logger.info("Employee not found in combination list")

      else: 
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.fact_del(conf.num_employee,itemid_main,"False")
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("We supply fired NO, where is the main employee card responce: " + response)
         
except:
   logger.info(sys.argv[0] + " ERROR")
    
