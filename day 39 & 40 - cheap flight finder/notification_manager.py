import requests
import os
import smtplib
from dotenv import load_dotenv


TEXTBEE_API_URL = "https://api.textbee.dev/api/v1"
SMTP_ADDRESS = "smtp.gmail.com"
load_dotenv("../../.env")


# This class is responsible for sending notifications with the deal flight details.
class NotificationManager:

    def __init__(self):
        self.textbee_api_url = TEXTBEE_API_URL
        self.textbee_api_key = os.getenv("TEXTBEE_API_KEY")
        self.textbee_phone_id = os.getenv("TEXTBEE_PHONE_ID")
        self.phone_number = None
        self.my_email = os.getenv('MY_TEST_EMAIL')
        self.my_email_pass = os.getenv('MY_TEST_EMAIL_PASS')

    def send_sms(self, message: str, msg_to="myself"):
        self.phone_number = os.getenv("PHONE_NUMBER")
        if msg_to != "myself":
            self.phone_number = msg_to
        rsp = requests.post(
            url=f'{self.textbee_api_url}/gateway/devices/{self.textbee_phone_id}/send-sms',
            json={'recipients': [self.phone_number], 'message': message},
            headers={'x-api-key': self.textbee_api_key}
        )
        rsp.raise_for_status()

    def send_emails(self, customers: list[dict], msg: str):
        with smtplib.SMTP(SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.my_email_pass)
            for customer in customers:
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=customer["whatIsYourEmail?"],
                    msg=f"Subject:Flight Alert!\n\n"
                        f"Hello {customer['whatIsYourFirstName?']} {customer['whatIsYourLastName?']},\n"
                        f"{msg}"
                )