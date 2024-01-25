import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Удаление Совместительства и Приема
try:
   df = db_conf.execute_sql(conf.del_parttime_sql)

   for row in df.itertuples():
       
      logger.info("Tabel number: " + row.tab_number)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_tab_number(conf.num_part,row.tab_number)
      logger.info("Find ItemID of an employee by tabel number in the combination list: " + itemid_main)
   #---------------------------------------------------------- 
      if itemid_main != "":
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.update_del_fact_gph(conf.num_part,itemid_main)
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("Update combination card responce" + response)
            
      else:
         ItemID = req_res.get_emp_by_tab_number(conf.num_employee,row.tab_number)
         logger.info("Find ItemID of an employee by tabel number in the list of employees: " + ItemID)

         if ItemID != "":
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.update_del_fact_gph(conf.num_employee,ItemID)
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("Employee card update responce responce" + response)
         else: 
            update = db_conf.update_sql(req_res.update_text_n_pa(row.s_count, row.id))
            logger.info("Employee not found")
         
except:
   logger.info(sys.argv[0] + " ERROR")
