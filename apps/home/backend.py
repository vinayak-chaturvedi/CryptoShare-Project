from tkinter import Y
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException
from clicksend_client import EmailRecipient
from clicksend_client import EmailFrom
from clicksend_client import Attachment
import json

from core.CoreLogic.mini_project_core import *

def send_sms(mobile):
    # Configure HTTP basic authorization: BasicAuth
    configuration = clicksend_client.Configuration()
    configuration.username = 'nocredit'
    configuration.password = 'D83DED51-9E35-4D42-9BB9-0E34B7CA85AE'

    # create an instance of the API class
    api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

    # If you want to explictly set from, add the key _from to the message.
    sms_message = SmsMessage(source="php",
                            body="Hello this is an api testing. This message has been sent by owls team.",
                            to="+91{}".format(mobile),
                            schedule=None)

    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

    try:
        # Send sms message(s)
        api_response = api_instance.sms_send_post(sms_messages)
        return 200
        
    except ApiException as e:
        return 400

def send_email(emailid, name):
    # Configure HTTP basic authorization: BasicAuth
    configuration = clicksend_client.Configuration()
    configuration.username = 'ritaj.sharma_cs.csf19@gla.ac.in'
    configuration.password = 'A3A4D064-525A-A0D8-4914-734325CE0E99'

    # create an instance of the API class
    api_instance = clicksend_client.TransactionalEmailApi(clicksend_client.ApiClient(configuration))
    email_receipient=EmailRecipient(email=emailid,name=name)
    email_from=EmailFrom(email_address_id='19829',name='CryptoShare')
    #attachment=Attachment(content='ZmlsZSBjb250ZW50cw==',
    #                      type='text/plain',
    #                      filename='text.txt',
    #                      disposition='attachment',
    #                      content_id='text')
    # Email | Email model
    email = clicksend_client.Email(to=[EmailRecipient(email=emailid,name=name)],
                                cc=[],
                                bcc=[],
                                _from=EmailFrom(email_address_id='19829',name='CryptoShare'),
                                subject="Email API Testing",
                                body="This is an email api testing. This message has been sent by the owls team",
                                #attachments=[attachment],
                                schedule=None) 

    try:
        # Send transactional email
        api_response = api_instance.email_send_post(email)
        return 200
    except ApiException as e:
        return 200



def encryptFile(fileDirectory, password):
    encryptor(fileDirectory, password)

def decryptFile(fileDirectory, password):
    Decryptor(fileDirectory, password)

def deleteDecrptedFile():
    pass