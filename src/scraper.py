from concurrent.futures import (
    ThreadPoolExecutor, 
    as_completed
)
from pathlib import Path
import typing as tp
import requests

from . import (
    api,
    storages,
    pages,
    dto
)


class NemezidaScraper:
    def __init__(self, img_storage_path: tp.Union[str, Path], json_storage_path: tp.Union[str, Path], threads=1) -> None:
        self._api = api.NemezidaApi()
        self._images_storage = storages.NemezidaImagesStorage(img_storage_path)
        self._json_storage = storages.NemezidaJsonStorage(json_storage_path)
        self._threads = threads
        self._thread_pool = ThreadPoolExecutor(max_workers=threads)
        
    def __del__(self):
        self._thread_pool.shutdown()
    
    def parse_search_pages_count(self) -> int:
        """
        Получаем первую страницу поиска и парсим кол-во страниц.
        """
        first_search_page_html = self._api.get_search_page()
        search_page = pages.SearchPage(first_search_page_html)
        pages_count = search_page.get_pages_count()
        return pages_count
    
    def parse_cards_urls_from_one_page(self, page: int) -> tp.List[str]:
        """
        Получаем страницу поиска по заданному номеру и парсим 
        ссылки на все, содержащиеся на ней карточки.
        """
        if page == 0:
            return []
        
        try:
            search_page_html = self._api.get_search_page(page)
        except requests.exceptions.HTTPError:
            return []
        
        search_page = pages.SearchPage(search_page_html)
        urls = search_page.get_cards_links()
        return urls
    
    def parse_card(self, url: str) -> tp.Optional[dto.ParsedCardData]:
        """
        Получаем страницу карточки по заданному url и парсим 
        все необходимые данные.
        """
        card_page_html = self._api.get_card_page(url)
        card_page = pages.CardPage(card_page_html)
        
        fullname = card_page.get_fullname()
        date = card_page.get_date()
        category = card_page.get_category()
        info = card_page.get_info()
        photos_urls = card_page.get_photos_urls()
        
        if not (fullname or date or category):
            return None

        return dto.ParsedCardData(fullname=fullname,
                                  date=date,
                                  category=category,
                                  info=info,
                                  photos_urls=photos_urls,
                                  url=url)

    def parse_cards_urls(self, from_page: int, to_page: int):
        """
        Получаем страницы поиска из заданного диапазона номеров и
        парсим ссылки на все, содержащеся на них ссылки на карточки 
        с использованием пула потоков.
        """
        futures = [self._thread_pool.submit(self.parse_cards_urls_from_one_page, page) 
                for page in range(from_page, to_page+1)]
        for future in as_completed(futures):
            for url in future.result():
                yield url
                

    def parse_cards(self, urls: tp.Iterable):
        """
        Получаем страницы карточек по заданному списку url и
        парсим все необходимые данные с использованием пула потоков.
        """
        futures = [self._thread_pool.submit(self.parse_card, url) 
                   for url in urls]
        for future in as_completed(futures):
            if future.result() is not None:
                yield future.result()
    
    def save_card(self, parsed_card: dto.ParsedCardData):
        """
        Сохраняем в хранилище данные и изображения одной карточки.
        """
        photos_ids = []
        for url in parsed_card.photos_urls:
            try:
                image_bytes = self._api.download_image(url)
            except Exception as ex:
                print(f'При сохранении изображения произошла ошибка\nURL:{url}\n{ex}')
                continue

            id = self._images_storage.save(image_bytes, url)
            photos_ids.append(id)
        
        card_for_save = dto.CardDataForSave(fullname=parsed_card.fullname,
                                            date=parsed_card.date,
                                            category=parsed_card.category,
                                            info=parsed_card.info,
                                            photos_ids=photos_ids,
                                            url=parsed_card.url)
        self._json_storage.save(card_for_save)
                
    def save_cards(self, parsed_cards: tp.Iterable):
        """
        Сохраняем в хранилище данные и изображения множества карточек.
        """
        for card in parsed_cards:
            try:
                self.save_card(card)
            except Exception as ex:
                print(f'При сохранении данных возникла ошибка:\n{ex}')
