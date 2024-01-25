import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Оформление ГПХ
try:
   df = db_conf.execute_sql(conf.gph_sql)

   for row in df.itertuples():
      
      logger.info("IIN: " + row.iin)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_iin(row.iin)
      logger.info("Find ItemID employee by IIN: " + itemid_main)
   #----------------------------------------------------------
      iin_mngr_itemid = req_res.ifnull(req_res.get_iin_mngr(row.iin_mngr))
      logger.info("Find iin_mngr: " + iin_mngr_itemid)
   #---------------------------------------------------------- 
      if itemid_main == "": 
         headers = get_xml_pa.get_header('CreateObject')
         body = get_xml_pa.create_employee(row.iin,
                                       row.tab_number, 
                                       row.fio,
                                       row.tel_number,
                                       row.phone, 
                                       row.employment, 
                                       row.mail,
                                       row.fio_en, 
                                       row.login,
                                       row.company, 
                                       row.subdivision,
                                       row.position,
                                       iin_mngr_itemid
                                       )
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Create employee responce: " + response)

      else: 
         headers = get_xml_pa.get_header('UpdateObject')
         body = get_xml_pa.update_employee(itemid_main,
                                       row.iin,
                                       row.tab_number, 
                                       row.fio,
                                       row.tel_number,
                                       row.phone, 
                                       row.employment,
                                       row.fio_en, 
                                       row.company, 
                                       row.subdivision,
                                       row.position,
                                       iin_mngr_itemid 
                                       )
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Update employee responce: " + response)
            
except:
    logger.info(sys.argv[0] + " ERROR")
    
