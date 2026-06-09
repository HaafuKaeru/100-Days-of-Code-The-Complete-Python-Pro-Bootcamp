import random
import smtplib
import datetime as dt


MY_EMAIL = "pythont090.test@gmail.com"
MY_PASSWORD = "lqkiwyqfzmzrtbgc"


now = dt.datetime.now()
week_day = now.weekday()

if week_day == 1:
    with open("quotes.txt") as quotes_file:
        all_quotes = quotes_file.readlines()
        quote = random.choice(all_quotes)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="python.receiver6543@outlook.com",
            msg=f"Subject:Quote of the day: {week_day}\n\n"
                f"{quote}")