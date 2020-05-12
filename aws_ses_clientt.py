import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from cm_util.cm_ssm_config import get_global_secret

import boto3

FORMAT = (
    "[%(levelname)s] %(asctime)-15s %(filename)s %(funcName)s "
    "%(threadName)s %(thread)d : %(message)s")

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# log_handler = logger.handlers[0]
# log_handler.setFormatter(logging.Formatter(FORMAT))

class AwsSESClient:
    ses_client = None

    def __init__(self):
        if self.ses_client is None:
            self.ses_client = boto3.client("ses")
            # self.from_mail_id = get_global_secret(" ")
            # self.to_mail_id = get_global_secret(" ")
            self.from_email_id = 'uday.turamandi@pilottravelcenters.com'
            self.to_email_id = 'uday.turamandi@pilottravelcenters.com'

    def send_email(self, subject,body):
        try:
            from_email = self.from_email_id
            to_email = self.to_email_id
            email_subject = subject
            email_body =body

            raw_message_data = self.get_email_data_with_attachment(
                email_subject, email_body, from_email, to_email)
            response = self.ses_client.send_raw_email(
                Source=from_email,
                Destinations=[to_email],
                RawMessage={'Data': raw_message_data.as_string()})
            print("Email send to {} having subject {}".format(
                to_email, email_subject))
            return response

        except Exception as e:
            print("Error while getting message data : {}".format(e))

    def get_email_data_with_attachment(self, subject, email_body, from_email, to_email):
        try:
            msg = MIMEMultipart('mixed')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email

            msg_body = MIMEMultipart('alternative')

            textpart = MIMEText(email_body.encode('utf-8'), 'plain', 'utf-8')
            htmlpart = MIMEText(email_body.encode('utf-8'), 'html', 'utf-8')

            msg_body.attach(textpart)
            msg_body.attach(htmlpart)

            msg.attach(msg_body)

            return msg
        except Exception as e:
            print("Error while getting email data : {}".format(e))
