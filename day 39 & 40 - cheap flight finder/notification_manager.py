import requests
import os


TEXTBEE_API_URL = "https://api.textbee.dev/api/v1"


# This class is responsible for sending notifications with the deal flight details.
class NotificationManager:

    def __init__(self):
        pass

    def api_post(self, message: str, msg_to="myself"):
        phone_number = os.getenv("PHONE_NUMBER")
        if msg_to != "myself":
            phone_number = msg_to
        rsp = requests.post(
            url=f'{TEXTBEE_API_URL}/gateway/devices/{os.getenv("TEXTBEE_PHONE_ID")}/send-sms',
            json={'recipients': [phone_number], 'message': message},
            headers={'x-api-key': os.getenv("TEXTBEE_API_KEY")}
        )
        rsp.raise_for_status()