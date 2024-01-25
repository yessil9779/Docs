import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Совместительство
try:
   df = db_conf.execute_sql(conf.parttime_sql)

   for row in df.itertuples():
      
      logger.info("IIN: " + row.iin)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_iin(row.iin)
      logger.info("Find employee ItemID by IIN: " + itemid_main)
   #---------------------------------------------------------- 
      subdivision_itemid = req_res.ifnull(req_res.get_subdivision(row.subdivision))
      logger.info("Find subdivision: " + subdivision_itemid)

      position_itemid = req_res.get_position(row.position)
      logger.info("Find position: " + position_itemid)

      iin_mngr_itemid = req_res.ifnull(req_res.get_iin_mngr(row.iin_mngr))
      logger.info("Find iin_mngr: " + iin_mngr_itemid)
   #---------------------------------------------------------- 
      if itemid_main != "":
         headers = get_xml_pa.get_header('FindObjects')
         body = get_xml_pa.find_objects_fired(conf.num_part,"[Табельный номер] = N'"+row.tab_number+"' AND [Deleted] = 0") 
         response = req_res.req(headers,body)
         logger.info("Find in the combination list responce : " + response)
         #----------------------------------------
         ItemID = req_res.check(response,'ItemID')
         Fired = req_res.check(response,'FieldStringValue') 
         logger.info("Find in the combination list ItemID и Fired : " + ItemID + " и " + Fired)

         if ItemID == "":
            headers = get_xml_pa.get_header('CreateObject')
            body = get_xml_pa.create_emp_part(row.tab_number,
                                          itemid_main, #fio
                                          row.employment,
                                          row.company, 
                                          subdivision_itemid, 
                                          position_itemid,
                                          iin_mngr_itemid
                                       )
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
            logger.info("Create an entry in the combination list : " + response)
         else:
            if Fired == "True":
               headers = get_xml_pa.get_header('UpdateObject')
               body = get_xml_pa.fact_del(conf.num_part,ItemID,"False")
               response = req_res.req(headers,body)
               update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
               logger.info("We put down the value where the field is dismissed YES: " + response)
            else: 
               update = db_conf.update_sql(req_res.update_text_n_pa(4, row.id))
               logger.info("Part-time data already exists")
            
      else:
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
                                       subdivision_itemid, 
                                       position_itemid,
                                       iin_mngr_itemid
                                       )
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Create a card if missing in the main query"+response)
         
except:
   logger.info(sys.argv[0] + " ERROR")
