from config import conf

def not_filled(str, par):
  if par in ("Не заполнено","0"): 
        return ""
  else:
        return str+'\n'

def get_header(method):
    header = {"content-type": "text/xml;charset=UTF-8",
              "SOAPAction": "http://tempuri.org/"+method}
    return header

#find_objects_body
def find_objects(listid,query):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
         <FindObjects xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      		<ListID>{listid}</ListID> 
     		 <Query>{query}</Query>
     	 <FieldNames />
    </FindObjects>
   </soapenv:Body>
</soapenv:Envelope>"""

# Delete Objects
def del_object(listid,itemid_main):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{listid}</ListID>
      <ItemID>{itemid_main}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>True</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------subdivion
def create_subdivion(org_name,org_desc_kaz,org_desc_rus,sap_id,company,subdivision_par_itemid,not_relevant):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <CreateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_subdivision}</ListID>
      <ItemFields>
        <ItemField>
          <FieldName>Название</FieldName>
          <FieldStringValue>{org_name}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Вербальное описание подразделения рус</FieldName>
          <FieldStringValue>{org_desc_rus}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Вербальное описание подразделения каз</FieldName>
          <FieldStringValue>{org_desc_kaz}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Номер SAP</FieldName>
          <FieldStringValue>{sap_id}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Компания</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{company}</LookupItemId>
            <LookupListId>{conf.num_company}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Родительское подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{subdivision_par_itemid}</LookupItemId>
            <LookupListId>17</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Не актуален с:</FieldName>
          <FieldStringValue>{not_relevant}</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </ItemFields>
      <ProcessSettingName />
      <ProcessUserName>erg\erg.shp-webapi</ProcessUserName>
    </CreateObject>
   </soapenv:Body>
</soapenv:Envelope>"""

def update_subdivion(itemid_main,org_name,org_desc_kaz,org_desc_rus,company,subdivision_par_itemid,not_relevant):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_subdivision}</ListID>
      <ItemID>{itemid_main}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Название</FieldName>
          <FieldStringValue>{org_name}</FieldStringValue>
          <OperationFlag />
        </ItemField>""" + '\n' \
        + not_filled("""<ItemField>
          <FieldName>Вербальное описание подразделения рус</FieldName>
          <FieldStringValue>{}</FieldStringValue>
          <OperationFlag />
        </ItemField>""".format(org_desc_rus),org_desc_rus) \
        + not_filled("""<ItemField>
          <FieldName>Вербальное описание подразделения каз</FieldName>
          <FieldStringValue>{}</FieldStringValue>
          <OperationFlag />
          </ItemField>""".format(org_desc_kaz),org_desc_kaz) \
        + not_filled("""<ItemField i:type="ItemLookupField">
          <FieldName>Компания</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{}</LookupItemId>
            <LookupListId>{}</LookupListId>
          </Item>
          </ItemField>""".format(company,conf.num_company),company) \
        + not_filled("""<ItemField i:type="ItemLookupField">
          <FieldName>Родительское подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{}</LookupItemId>
            <LookupListId>17</LookupListId>
          </Item>
          </ItemField>""".format(subdivision_par_itemid),subdivision_par_itemid) \
        + not_filled("""<ItemField>
          <FieldName>Не актуален с:</FieldName>
          <FieldStringValue>{}</FieldStringValue>
          <OperationFlag />
          </ItemField>""".format(not_relevant),not_relevant) \
        + """<ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------position
def create_position(org_name,org_desc_kaz,org_desc_rus,sap_id,not_relevant,relevant,subdivision_par_itemid,company):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <CreateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_position}</ListID>
      <ItemFields>
         <ItemField>
          <FieldName>Наименование должности</FieldName>
          <FieldStringValue>{org_name}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Вербальное описание должности рус</FieldName>
          <FieldStringValue>{org_desc_rus}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Вербальное описание должности каз</FieldName>
          <FieldStringValue>{org_desc_kaz}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>SAP ID должности</FieldName>
          <FieldStringValue>{sap_id}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Не актуален с:</FieldName>
          <FieldStringValue>{not_relevant}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Актуален с:</FieldName>
          <FieldStringValue>{relevant}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Родительское подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{subdivision_par_itemid}</LookupItemId>
            <LookupListId>17</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Компания</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{company}</LookupItemId>
            <LookupListId>{conf.num_company}</LookupListId>
          </Item>
        </ItemField>
      </ItemFields>
      <ProcessSettingName />
      <ProcessUserName>erg\erg.shp-webapi</ProcessUserName>
    </CreateObject>
   </soapenv:Body>
</soapenv:Envelope>"""

def update_position(itemid_main,org_name,org_desc_kaz,org_desc_rus,not_relevant,relevant,company,subdivision_par_itemid):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_position}</ListID>
      <ItemID>{itemid_main}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Наименование должности</FieldName>
          <FieldStringValue>{org_name}</FieldStringValue>
          <OperationFlag />
        </ItemField>""" + '\n' \
        + not_filled("""<ItemField>
          <FieldName>Вербальное описание должности рус</FieldName>
          <FieldStringValue>{}</FieldStringValue>
          <OperationFlag />
        </ItemField>""".format(org_desc_rus),org_desc_rus) \
        + not_filled("""<ItemField>
          <FieldName>Вербальное описание должности каз</FieldName>
          <FieldStringValue>{}</FieldStringValue>
          <OperationFlag />
          </ItemField>""".format(org_desc_kaz),org_desc_kaz) \
        + not_filled("""<ItemField>
          <FieldName>Не актуален с:</FieldName>
          <FieldStringValue>{}</FieldStringValue>
          <OperationFlag />
          </ItemField>""".format(not_relevant),not_relevant) \
        + not_filled("""<ItemField>
          <FieldName>Актуален с:</FieldName>
          <FieldStringValue>{}</FieldStringValue>
          <OperationFlag />
          </ItemField>""".format(relevant),relevant) \
        + not_filled("""<ItemField i:type="ItemLookupField">
          <FieldName>Компания</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{}</LookupItemId>
            <LookupListId>{}</LookupListId>
          </Item>
          </ItemField>""".format(company,conf.num_company),company) \
        + not_filled("""<ItemField i:type="ItemLookupField">
          <FieldName>Родительское подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{}</LookupItemId>
            <LookupListId>17</LookupListId>
          </Item>
          </ItemField>""".format(subdivision_par_itemid),subdivision_par_itemid) \
        + """<ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""