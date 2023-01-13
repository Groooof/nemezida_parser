from time import sleep
import schedule
from src.scraper import NemezidaScraper


def main():
    scraper = NemezidaScraper(threads=1)

    # pages_count = scraper.parse_search_pages_count()

    urls = scraper.parse_cards_urls(from_page=1, to_page=10)
    cards = scraper.parse_cards(urls)
    scraper.save_cards(cards)


if __name__ == '__main__':
    schedule.every(7).days.do(main).run()
    
    while 1:
        schedule.run_pending()
        sleep(1)


