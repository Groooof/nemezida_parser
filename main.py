from time import sleep
import schedule
from src.scraper import NemezidaScraper
from src import settings


def main():
    scraper = NemezidaScraper(threads=1,
                              img_storage_path=settings.IMAGES_STORAGE_FOLDER_PATH,
                              json_storage_path=settings.JSON_STORAGE_FOLDER_PATH)

    # pages_count = scraper.parse_search_pages_count() # общее кол-во страниц поиска

    urls = scraper.parse_cards_urls(from_page=1, to_page=10)
    cards = scraper.parse_cards(urls)
    scraper.save_cards(cards)

def test():
    for i in range(10):
        if i % 2 == 0: yield i


if __name__ == '__main__':
    # schedule.every(7).days.do(main).run() # запускать каждые 7 дней
    
    # while 1:
    #     schedule.run_pending()
    #     sleep(1)
    main()


