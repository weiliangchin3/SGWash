import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
import mimetypes
import os
from emailService import Create_Service


def sendEmail(name, email):

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg =  """
    <html>
        <body>
        <p>Hi {name}, </p> 
            <p> You have recently requested a service through SGWASH website and it is confirmed. </p >
            <p> Attached is the invoice for the transaction. </p> 
            <p> Thank you once again for using our services. See you again :) 
        </body>
    </html>
    """.format(name=name)

    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = email
    mimeMessage['subject'] = 'SGWASH SERVICE CONFIRMATION'
    mimeMessage.attach(MIMEText(emailMsg,'html'))

    file_attachments = ["SGWash-Invoice.pdf"]# In same directory as script

    for attachment in file_attachments:
        content_type, encoding = mimetypes.guess_type(attachment)
        main_type, sub_type = content_type.split('/', 1)
        file_name = os.path.basename(attachment)
    
        f = open(attachment, 'rb')
    
        myFile = MIMEBase(main_type, sub_type)
        myFile.set_payload(f.read())
        myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
        encoders.encode_base64(myFile)
    
        f.close()
    
        mimeMessage.attach(myFile)

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)