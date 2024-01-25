import sys,var
sys.path.append(var.folder)
#-----------------------------
from config import get_xml_om,db_conf,req_res,log,conf
#-----------------------------
logger = log.MyLogger(sys.argv[0])

try:
   df = db_conf.execute_sql(conf.om_sql)

   for row in df.itertuples():

      logger.info("Sap_id: " + row.sap_id)

      st_e = row.not_relevant
      st_end = st_e[:4]+"-"+st_e[4:6]+"-"+st_e[6:8]
      st_b = row.relevant
      st_beg = st_b[:4]+"-"+st_b[4:6]+"-"+st_b[6:8]

   #---------------------------------------------------------- position
      if row.event == 'S': 
         itemid_main = req_res.get_position(row.sap_id)
         logger.info("Find ItemID position: " + itemid_main)
   #---------
         subdivision_par_itemid = req_res.ifnull(req_res.get_subdivision(row.parent_dep_id))
         logger.info("Finding the parent department: " + subdivision_par_itemid)
   #--------- 
      
         if itemid_main == "": 
            headers = get_xml_om.get_header('CreateObject')
            body = get_xml_om.create_position(row.org_name,
                                          row.org_desc_kaz,
                                          row.org_desc_rus,
                                          row.sap_id,
                                          st_end,
                                          st_beg,
                                          subdivision_par_itemid,
                                          row.parent_comp_id
                                          )
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_om(response,row.s_count,row.id))
            logger.info("Create position responce: " + response)

         else: 
            headers = get_xml_om.get_header('UpdateObject')
            body = get_xml_om.update_position(itemid_main,
                                          row.org_name,
                                          row.org_desc_kaz,
                                          row.org_desc_rus,
                                          st_end,
                                          st_beg,
                                          row.parent_comp_id,
                                          subdivision_par_itemid
                                          )
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_om(response,row.s_count,row.id))
            logger.info("Update position responce: " + response)
   #---------------------------------------------------------- subdivision
      else: 
         itemid_main = req_res.get_subdivision(row.sap_id)
         logger.info("Find ItemID subdivision: " + itemid_main)
   #--------- 
         subdivision_par_itemid = req_res.ifnull(req_res.get_subdivision(row.parent_dep_id))
         logger.info("Finding the parent subdivision: " + subdivision_par_itemid)
   #---------
      
         if itemid_main == "": 
            headers = get_xml_om.get_header('CreateObject')
            body = get_xml_om.create_subdivion(row.org_name,
                                          row.org_desc_kaz,
                                          row.org_desc_rus,
                                          row.sap_id,
                                          row.parent_comp_id,
                                          subdivision_par_itemid,
                                          st_end
                                          )
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_om(response,row.s_count,row.id))
            logger.info("Create subdivision responce: " + response)

         else: 
            headers = get_xml_om.get_header('UpdateObject')
            body = get_xml_om.update_subdivion(itemid_main,
                                          row.org_name,
                                          row.org_desc_kaz,
                                          row.org_desc_rus,
                                          row.parent_comp_id,
                                          subdivision_par_itemid,
                                          st_end
                                          )
            response = req_res.req(headers,body)
            update = db_conf.update_sql(req_res.update_text_m_om(response,row.s_count,row.id))
            logger.info("Update subdivision responce: " + response)
      
except:
    logger.info(sys.argv[0] + " ERROR")
    
