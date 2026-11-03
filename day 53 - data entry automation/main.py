from web_scraping import ZillowScraper
from data_entry import GoogleFormManager


def main():

    scraper = ZillowScraper()
    listings = scraper.get_listings()

    form_manager = GoogleFormManager()
    for listing in listings:
        form_manager.submit_form(listing)
    form_manager.close()


if __name__ == '__main__':
    main()