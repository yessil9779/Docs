import xml.etree.ElementTree as ET
from app.conf import funcs, variables


#Универсальный сервис для передачи сведений о физических лицах по ИИН
def GBDFLUniversal_token(payload):
    IIN = payload['IIN']
    # get token
    token = funcs.get_jwt()
    # get kdp_xml
    kdp_xml = funcs.get_kdp_xml(IIN,token,"GBDFLUniversal_token")
    # get signed_wsse kdp
    signed_wsse = funcs.sign_wsse(kdp_xml)
    # send request to kdp
    headers = {'Content-Type': 'text/plain'}
    kdp_req = funcs.send_request(variables.shep_url, headers, signed_wsse)
    # get code_value and public_key_value
    root = ET.fromstring(kdp_req)
    namespace = {'ns3': 'http://service.2fa-chain.kz/ns/kdp'}
    public_key_element = root.find(".//ns3:public-key", namespace)
    code_element = root.find(".//ns3:code", namespace)
    code_value = code_element.text
    code_value = ''.join(code_value.split())
    public_key_value = public_key_element.text
    public_key_value = ''.join(public_key_value.split())
    # get_fl_xml
    get_fl_xml = funcs.get_fl_xml(IIN,code_value,public_key_value)
    # send req to fl
    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    main_req = funcs.send_request(variables.shep_url_external,headers,get_fl_xml)
    # generete responce api
    responce = funcs.get_responce_form(main_req)
    return responce


#Сервис предоставления регистрационных сведений о ЮЛ (филиале, представительстве) по БИН
def GbdulInfoByBin_v2(payload):
    BIN = payload['BIN']
    # get data form
    get_ul_data = funcs.get_ul_data(BIN)
    # sign data block
    signed_xml = funcs.sign_xml(get_ul_data)
    # get gbdul form
    get_ul_xml = funcs.get_ul_xml(signed_xml)
    # sign wsse gbdul xml
    signed_wsse = funcs.sign_wsse(get_ul_xml)
    # send request to shep
    headers = {'Content-Type': 'text/plain'}
    main_req = funcs.send_request(variables.shep_url, headers, signed_wsse)
    # generete responce api
    responce = funcs.get_responce_form(main_req)
    return responce

