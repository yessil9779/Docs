import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Удаление Соц.отпуск по беременности и родам/по уходу за ребенком до 3 лет
try:
   df = db_conf.execute_sql(conf.del_pregnant_sql)

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

      if Login.startswith("SAP") or Login.startswith("MYERG"):
         headers = get_xml_pa.get_header('UpdateObject')
         body = get_xml_pa.update_del_pregnant(conf.num_employee,itemid_main,row.employment)
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Update emplyee card responce" + response)

      else: 
         headers = get_xml_pa.get_header('UpdateObject')
         body = get_xml_pa.update_del_pregnant_else(conf.num_employee,itemid_main,False,row.employment)
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Update emplyee card responce" + response)
         
except:
    logger.info(sys.argv[0] + " ERROR")
    
