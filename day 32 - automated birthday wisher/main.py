##################### Extra Hard Starting Project ######################
import datetime as dt
import pandas as pd
import random
import smtplib


MY_EMAIL = "pythont090.test@gmail.com"
MY_PASSWORD = "xxx"
SMTP_ADDRESS = "smtp.gmail.com"

# 1. Update the birthdays.csv -> Done

# 2. Check if today matches a birthday in the birthdays.csv
now = dt.datetime.now()
this_year = now.year
this_month = now.month
this_day = now.day

data = pd.read_csv("birthdays.csv")
today_birthday = []
for index, entry in data.iterrows():
    if entry.month == this_month and entry.day == this_day:
        today_birthday.append(entry)

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
if today_birthday:
    for person in today_birthday:
        n = random.randint(1, 3)
        with open(f"letter_templates/letter_{n}.txt") as f:
            letter_text = f.read()
            letter_text = letter_text.replace("[NAME]", person["name"])
            letter_text = letter_text.replace("Angela", "Flavio")
# 4. Send the letter generated in step 3 to that person's email address.
        with smtplib.SMTP(SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=person["email"],
                msg=f"Subject:Happy Birthday!\n"
                    f"{letter_text}"
            )