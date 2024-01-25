import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
from bs4 import BeautifulSoup
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Расторжение ТД:
try:
   df = db_conf.execute_sql(conf.del_td_sql)

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
         logger.info("Find in the combination list responce : " + response)
         #----------------------------------------
         ItemID = req_res.check(response,'ItemID')
         logger.info("Find in the combination list ItemID: " + ItemID)

         if ItemID != "":
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.fact_del(conf.num_part,ItemID,"True")
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("Update in the combination list responce : " + response)
            
         else:
            update = db_conf.update_sql(req_res.update_text_n_pa(4, row.id))
            logger.info("Employee was not found in the combination list")    

      else: 
         headers = get_xml_pa.get_header('FindObjects')
         body = get_xml_pa.find_objects_fields(itemid_main)
         response = req_res.req(headers,body)
         soup_fields = BeautifulSoup(response, 'xml')
         logger.info("Find table values in combination list responce: " + response)
         #----------------------------------------
         ItemID = req_res.check(response,'ItemID')
         logger.info("Find ItemID table values in combination list: " + ItemID)
         #----------------------------------------
         try:
            FieldName_l = ["Компания","Подразделение","Должность (подстановка)","Руководитель"]
            LookupItemId = soup_fields.findAll('LookupItemId')
            data_l = {}
            for i in range(0,len(FieldName_l)):
               data_l[FieldName_l[i]] = LookupItemId[i].get_text()
         except: pass      
         #----------------------------------------
         try:
            FieldName_f = ["Компания","Подразделение","Занятость сотрудника","Должность (подстановка)","Табельный номер","Руководитель"]
            FieldStringValue = soup_fields.findAll('FieldStringValue')
            data_f = {}
            for i in range(0,len(FieldName_f)):
               data_f[FieldName_f[i]] = FieldStringValue[i].get_text()
         except: pass
         #----------------------------------------
         if len(FieldStringValue) != 0:
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.update_objects_combination(itemid_main,data_l['Компания'],data_l['Подразделение'],data_f['Занятость сотрудника'],data_l['Должность (подстановка)'],data_f['Табельный номер'],data_l['Руководитель'])
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("If present, then update the data in the main card responce: " + response)  
            #----------------------------------------
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.fact_del(conf.num_part,ItemID,"True")
            response = req_res.req(headers,body)
            logger.info("put down the value where the field is fired YES responce: " + response)

         else: 
            headers = get_xml_pa.get_header('UpdateObject')
            body = get_xml_pa.fact_del(conf.num_employee,itemid_main,"True")
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("We supply fired YES, where is the main employee card responce: " + response)
         
except:
   logger.info(sys.argv[0] + " ERROR")
    
