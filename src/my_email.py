import smtplib
import imaplib
import configparser
import email.parser
import email.header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailManager:

    def __init__(self):
        account = configparser.ConfigParser()
        account.read('../data/email/account.txt')
        self.email_address = account.get('account', 'address')
        self.email_password = account.get('account', 'password')
        domain_name = self.email_address.split('@')[1]
        
        servers = configparser.ConfigParser()
        servers.read("../data/email/mail_servers.txt")

        self.out_server = servers.get(domain_name, 'out_server')
        self.out_port = servers.get(domain_name, 'out_port')
        self.in_server = servers.get(domain_name, 'in_server')
        self.in_port = servers.get(domain_name, 'in_port')
        
    def sendMail(self, to, subject, message, attachments = None):
        try:
            server = smtplib.SMTP_SSL(host = self.out_server, port = self.out_port)
            # server.set_debuglevel(1)
            server.login(self.email_address, self.email_password)
            
            report = []
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            for address in to:
                msg['To'] = address
                server.send_message(msg, self.email_address, address)
                report.append(f"Message to {address} sent")
        except smtplib.SMTPAuthenticationError:
            report = "Incorrect user or password"
        except smtplib.SMTPRecipientsRefused:
            report = f"Recipient {msg['To']} refused"
        finally:
            server.quit()
        
        return report

    def getUnreadMails(self, inbox = 'INBOX'):
        try:
            server = imaplib.IMAP4_SSL(self.in_server, self.in_port)
            server.login(self.email_address, self.email_password)
            code, _ = server.select(inbox)
            if code != 'OK':
                report = f"Error, {inbox} is not a valid inbox name"
            else:
                code, result = server.search(None, '(UNSEEN)')
                unread = len(result[0].split())
                report = f"You have {unread} unread emails in your inbox {inbox}"
        except Exception as err:
            report = "Something wrong happen'd, may God help us!"
        
        return report

    def getUnreadMailsFrom(self, inbox = 'INBOX'):
        try:
            server = imaplib.IMAP4_SSL(self.in_server, self.in_port)
            server.login(self.email_address, self.email_password)
            code, _ = server.select(inbox)
            if code != 'OK':
                report = f"Error, {inbox} is not a valid inbox name"
            else:
                code, response = server.search(None, '(UNSEEN)')
                if code != 'OK':
                    report = "I have no idea what the hell hapen'd"
                else:
                    parser = email.parser.BytesHeaderParser()
                    report = ["You have no unread emails in your inbox."] \
                             if not response[0].split() else \
                             ["These are the unread mails in your inbox:"]
                    for i in response[0].split():
                        code, data = server.fetch(i, 'BODY.PEEK[HEADER]')
                        msg = parser.parsebytes(data[0][1], True)
                        text, _ = email.header.decode_header(msg['subject'])[0]
                        report.append(f"{msg['subject']} from {msg['from'].split('<')[0]}")
        except Exception as err:
            report = "Se produjo un error en la autenticacion"
        
        return report

# mailBox = EmailManager()
# print(mailBox.sendMail(["fgvolonterio@icloud.com",  "fgvolonterio@gmail.com"], "Test mail", "This is a test mail sent from python"))
# print(mailBox.getUnreadMails('INBOX'))
# print(mailBox.getUnreadMailsFrom('INBOX'))