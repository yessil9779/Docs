import requests
import hashlib
from requests_ntlm import HttpNtlmAuth

#hashlib.md5("test_str".encode('utf-8'), usedforsecurity=False).hexdigest()

headers = {"content-type": "text/xml;charset=UTF-8",
              "SOAPAction": "http://tempuri.org/FindObjects"}

body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
         <FindObjects xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      		<ListID>1</ListID> 
     		 <Query>[ИИН] = N'820907351581'</Query>
     	 <FieldNames />
    </FindObjects>
   </soapenv:Body>
</soapenv:Envelope>""" 

try:
    response = requests.post('https://smart.edms.erg.kz/_layouts/WSS/WSSC.V4.DMS.ERG.WebServices/WSSDocsWebApi.asmx',
                         data=body.encode('utf-8'),
                         headers=headers, 
                         auth=HttpNtlmAuth("erg.shp-webapi","fSjnwut4psmas!e"),
                         verify=r'/opt/nifi/scripts/esed/esed/src/cert/edms.pem')
    print(response.text)
except: pass


