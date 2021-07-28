import smtplib
import email.utils
from email.mime.text import MIMEText


class EmailManager:

    def __init__(self):
        self.email_address = None
        self.email_out_server = None
        self.email_in_server = None
        self.out_server_names = {
            'gmail.com':['smtp.gmail.com', 465],
            'hotmail.com':['smtp.live.com', 587],
            'outlook.com':['smtp.live.com', 587],
            'yahoo.com':['smtp.mail.yahoo.com', 465],
        }

    def sendMail(self, to, subject, message, attachments):
        msg = MIMEText(message)
        msg['From'] = self.email_address
        msg['Subject'] = subject

        try:
            for address in to:
                msg['To'] = address
                domain_name = address.split('@')[1]
                server_name = self.out_server_names[domain_name]
                if not server_name:
                    return f"Mail server {domain_name} not found."

                server = smtplib.SMTP(server_name[0], server_name[1])
                server.sendmail(self.email_address, [to], msg.as_bytes())
                # server.quit()
        finally:
            server.quit()
        
        return "Message sent"

    def recvMail(self, from):
        pass

    def recvMail(self):
        pass

    def addServer(self, host, smtp, port):
        self.out_server_names[host] = [ smtp, port ]