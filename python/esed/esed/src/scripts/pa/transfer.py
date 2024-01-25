import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_pa,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

#Постоянный/Временный перевод/Перемещение сотрудника:
try:
   df = db_conf.execute_sql(conf.transfer_sql)

   for row in df.itertuples():
      
      logger.info("Tabel number: " + row.tab_number)
   #---------------------------------------------------------- 
      itemid_main = req_res.get_emp_by_tab_number(conf.num_employee,row.tab_number)
      logger.info("Find employee ItemID by tabel number: " + itemid_main)
   #---------------------------------------------------------- 
      subdivision_itemid = req_res.ifnull(req_res.get_subdivision(row.subdivision))
      logger.info("Find subdivision: " + subdivision_itemid)

      position_itemid = req_res.get_position(row.position)
      logger.info("Find position: " + position_itemid)

      iin_mngr_itemid = req_res.ifnull(req_res.get_iin_mngr(row.iin_mngr))
      logger.info("Find iin_mngr: " + iin_mngr_itemid)
   #---------------------------------------------------------- 
      if itemid_main == "": 
         update = db_conf.update_sql(req_res.update_text_n_pa(row.s_count, row.id))
         logger.info("Employee not found")

      else: 
         headers = get_xml_pa.get_header('UpdateObject')
         body = get_xml_pa.update_transfer(itemid_main,
                                          row.company,
                                          subdivision_itemid,
                                          iin_mngr_itemid,
                                          position_itemid,
                                          row.employment
                                          )
         response = req_res.req(headers,body)
         update = db_conf.update_sql(req_res.update_text_m_pa(response,row.s_count,row.id))
         logger.info("Update employee: " + response)
         
except:
    logger.info(sys.argv[0] + " ERROR")
    
