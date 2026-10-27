import os
import dotenv
import smtplib

from email.message import EmailMessage


dotenv.load_dotenv("../.env")


def message_body(name: str, price: float, link: str) -> str:
    message = EmailMessage()
    message['From'] = "PythonBot"
    message['Subject'] = "Amazon Price Alert!"
    message.set_content(
        f"The '{name}' is now ${price}\n"
        f"{link}"
    )
    return message.as_string()


class NotificationManager:

    def __init__(self):
        self.smtp_address = os.getenv("smtp_address")
        self.sender_email = os.getenv("my_test_email")
        self.sender_email_pass = os.getenv("my_test_email_pass")
        self.my_email = os.getenv("my_email")

    def send_email(self, msg: str):
        with smtplib.SMTP(self.smtp_address) as connection:
            connection.starttls()
            connection.login(user=self.sender_email, password=self.sender_email_pass)
            connection.sendmail(
                from_addr=self.sender_email,
                to_addrs=self.my_email,
                msg=msg
            )