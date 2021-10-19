from Google import Create_Service
import base64
import mimetypes
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import httplib2.error
from time import sleep


class Attachment:
    def __init__(self, path: str = None, name: str = None):
        self.name = name
        if self.name is None:
            self.name = os.path.basename(path)
        content_type, encoding = mimetypes.guess_type(path)
        self.main_type, self.ext = content_type.split('/', 1)
        try:
            file = open(path, 'rb')

            self.myFile = MIMEBase(self.main_type, self.ext)
            self.myFile.set_payload(file.read())
            self.myFile.add_header('Content-Disposition', 'attachment', filename=name)
            encoders.encode_base64(self.myFile)

            file.close()
        except FileNotFoundError:
            print('Такого файла не существует')


class Sender(Attachment):
    def __init__(self, subject: str = None, receiver: str = None,
                 content: str = None, file_path: str = None, file_name: str = None):
        self.service = Create_Service('json/credentials.json', 'gmail', 'v1',
                                      ['https://www.googleapis.com/auth/gmail.send'])
        self.mimeMessage = MIMEMultipart()
        self.mimeMessage['to'] = receiver
        if subject is not None:
            self.mimeMessage['subject'] = subject
        if content is not None:
            self.mimeMessage.attach(MIMEText(content, 'plain'))
        if file_path is not None:
            super().__init__(path=file_path, name=file_name)
            if hasattr(self, 'myFile'):
                self.mimeMessage.attach(self.myFile)

    def send(self):
        raw_string = base64.urlsafe_b64encode(self.mimeMessage.as_bytes()).decode()
        try:
            self.service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        except httplib2.error.ServerNotFoundError:
            sleep(30)
            self.send()
        except AttributeError:
            print('Введите хотя бы что-то')
