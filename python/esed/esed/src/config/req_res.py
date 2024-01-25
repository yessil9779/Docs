import requests
import sys
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
from config import get_xml_pa,conf,log

logger = log.MyLogger(sys.argv[0])

def req(headers,body):
        try:
            response = requests.post(conf.url,data=body.encode('utf-8'),headers=headers, auth=HttpNtlmAuth(conf.esed_username,conf.esed_password),verify=conf.cert_path)
            return response.text
        except requests.exceptions.HTTPError as e:
            logger.info("HTTPError: "+str(e))
        except requests.exceptions.RequestException as e:
            logger.info("RequestException: "+str(e))
        except:
            logger.info("GET REQUEST ERROR")

#GetXmlTag
def check(response,tag):
    soup = BeautifulSoup(response, 'xml')
    try:
       return soup.find(tag).text
    except: return ""

#Check if null
def ifnull(txt):
    if txt == "" or txt is None:
        txt = "0"
    return txt

#Check responce code
def c_code(response):
    code = check(response,'OperationResult')
    if code == "true":
        return "200"
    else: 
        return "404"
#------------------------------------------------------------------
#Поиск компании
def get_company(company_itemid):
        try:
            headers = get_xml_pa.get_header('FindObjects')
            company_body = get_xml_pa.find_objects(conf.num_company,"[Номер SAP] = N'"+company_itemid+"'") 
            response = req(headers,company_body)
            company_itemid = check(response,'ItemID')
            return company_itemid
        except:
            logger.info("GET subdivision eroor")

#Поиск подразделении
def get_subdivision(subdivision_itemid):
        try:
            headers = get_xml_pa.get_header('FindObjects')
            subdivision_body = get_xml_pa.find_objects(conf.num_subdivision,"[Номер SAP] = N'"+subdivision_itemid+"'") 
            response = req(headers,subdivision_body)
            subdivision_itemid = check(response,'ItemID')
            return subdivision_itemid
        except:
            logger.info("GET subdivision eroor")

#Поиск должности
def get_position(position_itemid):
        try:
            headers = get_xml_pa.get_header('FindObjects')
            position_body = get_xml_pa.find_objects(conf.num_position,"[SAP ID должности] = N'"+position_itemid+"'")
            response = req(headers,position_body)
            position_itemid = check(response,'ItemID')
            return position_itemid
        except:
            logger.info("GET position eroor")

#Поиск руководителя
def get_iin_mngr(iin_mngr_itemid):
        try:
            headers = get_xml_pa.get_header('FindObjects')
            iin_mngr_body = get_xml_pa.find_objects(conf.num_employee," [ИИН] = N'"+iin_mngr_itemid+"'") 
            response = req(headers,iin_mngr_body)
            iin_mngr_itemid = check(response,'ItemID')
            return iin_mngr_itemid
        except:
            logger.info("GET iin_mngr eroor")

#Поиск по карточкам сотрудников по ИИН
def get_emp_by_iin(iin):
        try:
            headers = get_xml_pa.get_header('FindObjects')
            body = get_xml_pa.find_objects(conf.num_employee,"[ИИН] = N'"+iin+"'") 
            response = req(headers,body)
            iin_itemid = check(response,'ItemID')
            return iin_itemid
        except:
            logger.info("GET emp_by_iin eroor")

#Поиск по карточкам сотрудников по табельному номеру
def get_emp_by_tab_number(listid,tab_number):
        try:
            headers = get_xml_pa.get_header('FindObjects')
            body = get_xml_pa.find_objects(listid,"[Табельный номер] = N'"+tab_number+"'") 
            response = req(headers,body)
            tab_number_itemid = check(response,'ItemID')
            return tab_number_itemid
        except:
            logger.info("GET emp_by_tab_number eroor")


def update_text_n_om(id):
    sql = '''update "HR_MI086"."agg_om_table" set status_code = '404', status_text = 'Not found!', s_count = 4 where id = {}'''.format(id)
    return sql

def update_text_m_om(response,s_count,id):
    sql = '''update "HR_MI086"."agg_om_table" set status_code = '{}', status_text = '{}', s_count = {} where id = {}'''.format(c_code(response),response,s_count+1,id)
    return sql

def update_text_n_pa(s_count,id):
    sql = '''update "HR_MI086"."agg_pa_table" set status_code = '404', status_text = 'Сотрудник не найден', s_count = {} where id = {}'''.format(s_count+1, id)
    return sql

def update_text_m_pa(response,s_count,id):
    sql = '''update "HR_MI086"."agg_pa_table" set status_code = '{}', status_text = '{}', s_count = {} where id = {}'''.format(c_code(response),response,s_count+1,id)
    return sql