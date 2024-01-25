from config import conf

#получить header запроса
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
#----------------------------------------------------------------------accept
#Создание карточки сотрудника 
def create_employee(iin,tab_number,fio,tel_number,phone,employment,mail,fio_en,login,company,subdivision,position,iin_mngr):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <CreateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_employee}</ListID>
      <ItemFields>
        <ItemField>
          <FieldName>ИИН</FieldName>
          <FieldStringValue>{iin}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Табельный номер</FieldName>
          <FieldStringValue>{tab_number}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Имя пользователя</FieldName>
          <FieldStringValue>{fio}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Телефон</FieldName>
          <FieldStringValue>{tel_number}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Сотовый телефон</FieldName>
          <FieldStringValue>{phone}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField> 
        <ItemField>
          <FieldName>Адрес электронной почты</FieldName>
          <FieldStringValue>{mail}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Имя пользователя EN</FieldName>
          <FieldStringValue>{fio_en}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Логин</FieldName>
          <FieldStringValue>{login}</FieldStringValue>
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
          <FieldName>Подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{subdivision}</LookupItemId>   
            <LookupListId>{conf.num_subdivision}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Должность (подстановка)</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{position}</LookupItemId>
            <LookupListId>{conf.num_position}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Руководитель</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{iin_mngr}</LookupItemId>   
            <LookupListId>{conf.num_employee}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>True</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </ItemFields>
      <ProcessSettingName />
      <ProcessUserName>erg\erg.shp-webapi</ProcessUserName>
    </CreateObject>
   </soapenv:Body>
</soapenv:Envelope>"""

#Обновление карточки сотрудника
def update_employee(itemid_main,iin,tab_number,fio,tel_number,phone,employment,fio_en,company,subdivision,position,iin_mngr):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_employee}</ListID>
      <ItemID>{itemid_main}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>ИИН</FieldName>
          <FieldStringValue>{iin}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Табельный номер</FieldName>
          <FieldStringValue>{tab_number}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Имя пользователя</FieldName>
          <FieldStringValue>{fio}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Телефон</FieldName>
          <FieldStringValue>{tel_number}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Сотовый телефон</FieldName>
          <FieldStringValue>{phone}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField> 
        <ItemField>
          <FieldName>Имя пользователя EN</FieldName>
          <FieldStringValue>{fio_en}</FieldStringValue>
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
          <FieldName>Подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{subdivision}</LookupItemId>
            <LookupListId>{conf.num_subdivision}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Должность (подстановка)</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{position}</LookupItemId>
            <LookupListId>{conf.num_position}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Руководитель</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{iin_mngr}</LookupItemId>
            <LookupListId>{conf.num_employee}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------parttime
#Создание карточки совмещения
def create_emp_part(tab_number,fio,employment,company,subdivision,position,iin_mngr):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <CreateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_part}</ListID>
      <ItemFields>
        <ItemField>
          <FieldName>Табельный номер</FieldName>
          <FieldStringValue>{tab_number}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Имя пользователя</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{fio}</LookupItemId>
            <LookupListId>{conf.num_employee}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
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
          <FieldName>Подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{subdivision}</LookupItemId>
            <LookupListId>{conf.num_subdivision}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Должность (подстановка)</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{position}</LookupItemId>
            <LookupListId>{conf.num_position}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Руководитель</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{iin_mngr}</LookupItemId>
            <LookupListId>{conf.num_employee}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </ItemFields>
      <ProcessSettingName />
      <ProcessUserName>erg\erg.shp-webapi</ProcessUserName>
    </CreateObject>
   </soapenv:Body>
</soapenv:Envelope>"""

#Признак уволен
def fact_del(listid,itemid,fired):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{listid}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>{fired}</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""

#Найти объект где поле уволен
def find_objects_fired(listid,query):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
         <FindObjects xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      		<ListID>{listid}</ListID> 
     		 <Query>{query}</Query>
     	<FieldNames>
        <string>Уволен</string>
      </FieldNames>
    </FindObjects>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------td_del
#Найти значения таблицы Совмещение
def find_objects_fields(itemid):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <FindObjects xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_part}</ListID> 
      <Query>[Имя пользователя] = {itemid} AND [Уволен] = 'False'</Query>
      <FieldNames>
        <string>Компания</string>
        <string>Подразделение</string>
        <string>Занятость сотрудника</string>
        <string>Должность (подстановка)</string>
        <string>Табельный номер</string>
        <string>Руководитель</string>
      </FieldNames>
    </FindObjects>
   </soapenv:Body>
</soapenv:Envelope>"""

def update_objects_combination(itemid,company,subdivision,employment,position,tab_number,iin_mngr):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_employee}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField i:type="ItemLookupField">
          <FieldName>Компания</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{company}</LookupItemId>
            <LookupListId>{conf.num_company}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{subdivision}</LookupItemId>
            <LookupListId>{conf.num_subdivision}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField> 
        <ItemField i:type="ItemLookupField">
          <FieldName>Должность (подстановка)</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{position}</LookupItemId>
            <LookupListId>{conf.num_position}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Табельный номер</FieldName>
          <FieldStringValue>{tab_number}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Руководитель</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{iin_mngr}</LookupItemId>
            <LookupListId>{conf.num_employee}</LookupListId>
          </Item>
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------transfer
#Обновление карточки сотрудника
def update_transfer(itemid,company,subdivision,iin_mngr,position,employment):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_employee}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField i:type="ItemLookupField">
          <FieldName>Компания</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{company}</LookupItemId>
            <LookupListId>{conf.num_company}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Подразделение</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{subdivision}</LookupItemId>
            <LookupListId>{conf.num_subdivision}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Руководитель</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{iin_mngr}</LookupItemId>
            <LookupListId>{conf.num_employee}</LookupListId>
          </Item>
        </ItemField>
        <ItemField i:type="ItemLookupField">
          <FieldName>Должность (подстановка)</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{position}</LookupItemId>
            <LookupListId>{conf.num_position}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------change
def update_change(itemid,iin,fio,tel_number,phone,fio_en):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_employee}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>ИИН</FieldName>
          <FieldStringValue>{iin}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Имя пользователя</FieldName>
          <FieldStringValue>{fio}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Телефон</FieldName>
          <FieldStringValue>{tel_number}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Сотовый телефон</FieldName>
          <FieldStringValue>{phone}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Имя пользователя EN</FieldName>
          <FieldStringValue>{fio_en}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------del_gph, del_fact
def update_del_fact_gph(listid,itemid):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{listid}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField i:type="ItemLookupField">
          <FieldName>Должность (подстановка)</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>0</LookupItemId>
            <LookupListId>{conf.num_position}</LookupListId>
          </Item>
        </ItemField>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>True</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------early_exit
def find_login_tabnumber(tab_number):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
         <FindObjects xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      		<ListID>{conf.num_employee}</ListID> 
     		 <Query>[Табельный номер] = N'{tab_number}'</Query>
     	 <FieldNames>
          <string>Логин</string>
         </FieldNames>
    </FindObjects>
   </soapenv:Body>
</soapenv:Envelope>"""
#------------------------
def update_early_exit(itemid,employment,relevant):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{conf.num_employee}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField> 
        <ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>{relevant}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Уволен</FieldName>
          <FieldStringValue>False</FieldStringValue>
          <OperationFlag />
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------_del_early_exit
def update_del_early_exit(listid,itemid,employment):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{listid}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField> 
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------_del_pregnant
def update_del_pregnant(listid,itemid,employment):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{listid}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField> 
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#-----------------
def update_del_pregnant_else(listid,itemid,fired,employment):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{listid}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField>
          <FieldName>Не актуален</FieldName>
          <FieldStringValue>{fired}</FieldStringValue>
          <OperationFlag />
        </ItemField>
        <ItemField>
          <FieldName>Занятость сотрудника</FieldName>
          <FieldStringValue>{employment}</FieldStringValue>
          <OperationFlag />
        </ItemField> 
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""
#----------------------------------------------------------------------update_iin_mngr
def update_iin_mngr(listid,itemid,iin_mngr):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
    <UpdateObject xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://tempuri.org/">
      <ListID>{listid}</ListID>
      <ItemID>{itemid}</ItemID>
      <Fields>
        <ItemField i:type="ItemLookupField">
          <FieldName>Руководитель</FieldName>
          <OperationFlag />
          <Item>
            <LookupItemId>{iin_mngr}</LookupItemId>
            <LookupListId>1</LookupListId>
          </Item>
        </ItemField>
      </Fields>
    </UpdateObject>
   </soapenv:Body>
</soapenv:Envelope>"""