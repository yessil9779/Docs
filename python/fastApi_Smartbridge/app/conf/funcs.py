import requests
import json
import datetime
import jwt
import base64
import secrets
from app.conf import variables
from xml.sax.saxutils import escape
from cryptography.hazmat.primitives.serialization import pkcs12
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


def validate_credentials(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    input_user_name = credentials.username.encode("utf-8")
    input_password = credentials.password.encode("utf-8")
    stored_username = variables.auth_username
    stored_password = variables.auth_password
    is_username = secrets.compare_digest(input_user_name, stored_username)
    is_password = secrets.compare_digest(input_password, stored_password)
    if is_username and is_password:
        return {"auth message": "authentication successful"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials",
                        headers={"WWW-Authenticate": "Basic"})

def get_responce_form(xml):
    responce = {
        "Status": "Success",
        "Date_time": datetime.now(),
        "xml": xml
    }
    return responce

def get_ul_data(BIN):
    ul_data = f'<ns2:Request xmlns:ns2="http://gbdulinfobybin_v2.egp.gbdul.tamur.kz"><RequestorBIN>{variables.BTS_BIN}</RequestorBIN><BIN>{BIN}</BIN></ns2:Request>'
    return ul_data

def get_ul_xml(xml):
    ul_xml = f'<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"><SOAP-ENV:Header xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\"></SOAP-ENV:Header><soap:Body xmlns:wsu=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\" wsu:Id=\"id-17045db8-14bf-4ac0-9755-11baa05459a5\"><ns2:SendMessage xmlns:ns2=\"http://bip.bee.kz/SyncChannel/v10/Types\"><request><requestInfo><messageId>987916b1-d192-48ad-9487-965ab70483a4</messageId><serviceId>GbdulInfoByBin_v2</serviceId><messageDate>2022-09-21T17:42:45.492+06:00</messageDate><sender><senderId>{variables.senderId}</senderId><password>{variables.senderPass}</password></sender></requestInfo><requestData><data xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance\">{xml}</data></requestData></request></ns2:SendMessage></soap:Body></soap:Envelope>'
    return ul_xml

def get_kdp_xml(iin, token, access_name):
    kdp_xml = f'<?xml version="1.0" encoding="UTF-8"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"><SOAP-ENV:Header xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\"></SOAP-ENV:Header><soap:Body xmlns:wsu=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\" wsu:Id=\"id-17045db8-14bf-4ac0-9755-11baa05459a5\"><ns2:SendMessage xmlns:ns2=\"http://bip.bee.kz/SyncChannel/v10/Types\"><request><requestInfo><messageId>4579ed7a-8a17-4c6c-9cf6-c637f15b8b7f</messageId><correlationId>efd82b8a-3f40-4a22-a417-089ec719e02a</correlationId><serviceId>KDP_SERVICE</serviceId><messageDate>2023-05-17T00:05:37.002+06:00</messageDate><sender><senderId>{variables.senderId}</senderId><password>{variables.senderPass}</password></sender></requestInfo><requestData><data xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance\"><uin>{iin}</uin><company>{variables.company}</company><company_bin>{variables.BTS_BIN}</company_bin><company_responsible>Ministry_of_Justice_of_the_Republic_of_Kazakhstan</company_responsible><employee_name>Karibayev_Azamat_Ramazanovich</employee_name><access_name>{access_name}</access_name><personal_data_name>adress</personal_data_name><expiresIn>132000000</expiresIn><omit-sms>true</omit-sms><ovt>{token}</ovt></data></requestData></request></ns2:SendMessage></soap:Body></soap:Envelope>'
    return kdp_xml

def get_fl_xml(iin,code_value,public_key_value):
    fl_xml = f'<?xml version="1.0" encoding="UTF-8"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"><SOAP-ENV:Header xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\"></SOAP-ENV:Header><soap:Body xmlns:wsu=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\" wsu:Id=\"id-17045db8-14bf-4ac0-9755-11baa05459a5\"><ns2:SendMessage xmlns:ns2=\"http://bip.bee.kz/SyncChannel/v10/Types\"><request><requestInfo><messageId>c5r93skf5g1a8t38tlpg</messageId><serviceId>GBDFLUniversal_token</serviceId><messageDate>2021-10-25T11:16:02Z</messageDate><sender><senderId>{variables.senderId}</senderId><password>{variables.senderPass}</password></sender><sessionId>c5r93skf5g1a8t38tlpg</sessionId></requestInfo><requestData><data xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance\"><messageId>c5r93skf5g1a8t38tlpg</messageId><messageDate>2021-10-25T11:16:02Z</messageDate><senderCode>{variables.senderCode}</senderCode><iin>{iin}</iin><kdpToken>{code_value}</kdpToken><publicKey>{public_key_value}</publicKey></data></requestData></request></ns2:SendMessage></soap:Body></soap:Envelope>'
    return fl_xml

def sign_xml(xml_data):
    url = variables.sign_url
    xml = xml_data
    payload = json.dumps({"xml": xml,
                          "signers": [{
                          "key": variables.key_sign_data,
                          "password":variables.password_sign_data
                                      }]
                          })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    return escape(data['xml'])

def sign_wsse(xml):
    xml = xml
    url = variables.wsse_url

    payload = json.dumps({
        "xml": xml,
        "key": variables.key_tp,
        "password": variables.password_tp
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    return data['xml']


def send_request(url,headers, payload):
    payload = payload
    headers = headers
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

def get_jwt():
    due_date = datetime.now() + timedelta(minutes=600)
    expiry = int(due_date.timestamp())
    iat = int(datetime.now().timestamp())

    p12_key = base64.b64decode(variables.key_jwt)
    p12_password = variables.password_jwt

    payload = {"cbin": variables.BTS_BIN,
               "mcheck": "Bio",
               "iat": iat,
               "exp": expiry}

    key, cert, add_cert = pkcs12.load_key_and_certificates(p12_key, p12_password)

    token = jwt.encode(payload, key, algorithm='RS256')
    return token