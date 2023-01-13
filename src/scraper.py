from concurrent.futures import (
    ThreadPoolExecutor, 
    as_completed
)
import typing as tp

from . import (
    api,
    storages,
    pages,
    dto
)


class NemezidaScraper:
    def __init__(self, threads=1) -> None:
        self._api = api.NemezidaApi()
        self._images_storage = storages.ImagesStorage('./images')
        self._json_storage = storages.JsonStorage('./data')
        self._threads = threads
        self._thread_pool = ThreadPoolExecutor(max_workers=threads)
        
    def __del__(self):
        self._thread_pool.shutdown()
    
    def parse_search_pages_count(self) -> int:
        first_search_page_html = self._api.get_search_page()
        search_page = pages.SearchPage(first_search_page_html)
        pages_count = search_page.get_pages_count()
        return pages_count
    
    def parse_cards_urls_from_one_page(self, page: int) -> tp.List[str]:
        search_page_html = self._api.get_search_page(page)
        search_page = pages.SearchPage(search_page_html)
        urls = search_page.get_cards_links()
        return urls
    
    def parse_card(self, url: str) -> dto.ParsedCardData:
        card_page_html = self._api.get_card_page(url)
        card_page = pages.CardPage(card_page_html)
        
        fullname = card_page.get_fullname()
        date = card_page.get_date()
        category = card_page.get_category()
        info = card_page.get_info()
        photos_urls = card_page.get_photos_urls()

        return dto.ParsedCardData(fullname=fullname,
                              date=date,
                              category=category,
                              info=info,
                              photos_urls=photos_urls)

    def parse_cards_urls(self, from_page: int, to_page: int):
        futures = [self._thread_pool.submit(self.parse_cards_urls_from_one_page, page) 
                for page in range(from_page, to_page+1)]
        for future in as_completed(futures):
            for url in future.result():
                yield url
                

    def parse_cards(self, urls: tp.Iterable):
        futures = [self._thread_pool.submit(self.parse_card, url) 
                   for url in urls]
        for future in as_completed(futures):
            yield future.result()
                
    def save_card(self, parsed_card: dto.ParsedCardData):
        photos_ids = []
        for url in parsed_card.photos_urls:
            image_bytes = self._api.get_image(url)
            id = self._images_storage.save(image_bytes)
            photos_ids.append(id)
        
        card_for_save = dto.CardDataForSave(fullname=parsed_card.fullname,
                                        date=parsed_card.date,
                                        category=parsed_card.category,
                                        info=parsed_card.info,
                                        photos_ids=photos_ids)
        self._json_storage.save(card_for_save.as_dict())
                
    def save_cards(self, parsed_cards: tp.Iterable):
        for card in parsed_cards:
            self.save_card(card)