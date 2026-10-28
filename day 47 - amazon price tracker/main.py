from web_scraper import AmazonScraper
from notification_manager import NotificationManager, message_body


STATIC_URL = "https://appbrewery.github.io/instant_pot/"  # for test
LIVE_URL = "https://www.amazon.com/Instant-Pot-Electric-Sterilizer-Stainless/dp/B09MZTP44L?nsdOptOutParam=true"
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