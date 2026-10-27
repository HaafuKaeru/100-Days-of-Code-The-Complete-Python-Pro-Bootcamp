from web_scraper import AmazonScraper
from notification_manager import NotificationManager, message_body


STATIC_URL = "https://appbrewery.github.io/instant_pot/"  # for test
LIVE_URL = "https://www.amazon.com/Instant-Pot-Electric-Sterilizer-Stainless/dp/B09MZTP44L?crid=XZIUKDAXDCU&dib=eyJ2IjoiMSJ9.SP20oqKtdFL49e0JOMm60DW4FyiAXLCV13aW6jiuOksQ6dTgp3O8h14t7stmXdi3wa-7ei1Mvme0Pcr2hEeed24-JS1G6TcqvTp3kdBTMuCdEP7usFMP2-STmk3FyKKmwW3zCXCAvr0ihRYPXvuYQMJLZbB5UKroYtslxXUS6Uwl7ypuK044051IEjawwg9rNJRxK5GUU5ts__ay0IBYgmfU2KjyV6ukwj3Oxvi79fE.dlAHKlrEYPeC3xDEe6_A4n1goKs4Qya0jTotfu1kUC4&dib_tag=se&keywords=Instant+Pot+Duo+Plus+9-in-1+Electric+Pressure+Cooker&nsdOptOutParam=true&qid=1793115855&sprefix=instant+pot+duo+plus+9-in-1+electric+pressure+cooker%2Caps%2C181&sr=8-1"
TARGET_PRICE = 120.00


def main():

    url = LIVE_URL
    scraper = AmazonScraper(url)
    product_name = scraper.get_product_name()
    price = scraper.get_price()

    if price < TARGET_PRICE:
        notification_manager = NotificationManager()
        notification_manager.send_email(message_body(product_name, price, url))


if __name__ == '__main__':
    main()