from time import sleep
import schedule
from src.scraper import NemezidaScraper
from src.engine import RequestsEngine
from src import settings
from src import callbacks


def main():
    engine = RequestsEngine(default_timeout=10,
                            default_retries=10,
                            before_request=callbacks.before_request,
                            after_request=callbacks.after_request,
                            on_exception=callbacks.on_request_exception)
    
    scraper = NemezidaScraper(engine=engine,
                              threads=settings.THREADS_COUNT,
                              img_storage_path=settings.IMAGES_STORAGE_FOLDER_PATH,
                              json_storage_path=settings.JSON_STORAGE_FOLDER_PATH)

    # pages_count = scraper.parse_search_pages_count() # общее кол-во страниц поиска

    print(f'----------------------')
    print(f'Парсер начинает работу')
    print(f'Страницы:\tс {settings.FROM_PAGE} по {settings.TO_PAGE}')
    print(f'Кол-во потоков:\t{settings.THREADS_COUNT}')
    print(f'Изображения будут сохранены в:\t{settings.IMAGES_STORAGE_FOLDER_PATH}')
    print(f'Данные будут сохранены в:\t{settings.JSON_STORAGE_FOLDER_PATH}')
    print(f'----------------------')
    
    urls = scraper.parse_cards_urls(from_page=settings.FROM_PAGE, to_page=settings.TO_PAGE)
    cards = scraper.parse_cards(urls)
    count = scraper.save_cards(cards)
    print('Парсер закончил работу')
    print(f'Собрано карточек: {count}')


if __name__ == '__main__':
    schedule.every(7).days.do(main).run() # запускать каждые 7 дней
    
    while 1:
        schedule.run_pending()
        sleep(1)


