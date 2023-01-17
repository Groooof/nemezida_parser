from time import sleep
import typing as tp 
import requests

from .engine import RequestsEngine


class BaseApi:
    """
    Базовый класс для работы с API какого-либо сайта/сервиса.
    """
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.838 Yowser/2.5 Safari/537.36'}

    def __init__(self, engine: RequestsEngine) -> None:
        self._request = engine.request
            

class BaseImageDownloadApi(BaseApi):
    def download_image(self, url: str) -> bytes:
        resp = self._request(requests.get, url)
        return resp.content


class NemezidaApi(BaseImageDownloadApi):
    """
    Класс для работы с API сайта nemez1da.ru.
    """
    
    main_url = 'https://nemez1da.ru'
    
    def get_search_page(self, page: tp.Union[str, int] = 1) -> str:
        """
        Получает содержание поисковой страницы по её номеру.
        """
        url = self.generate_search_page_url(page)
        resp = self._request(requests.get, url, headers=self.headers)
        return resp.text
    
    def get_card_page(self, url: str) -> str:
        resp = self._request(requests.get, url, headers=self.headers)
        return resp.text
    
    def generate_search_page_url(self, page: tp.Union[int, str]) -> str:
        """
        Формирует ссылку на страницу поиска по её номеру.
        """
        return self.main_url + '/page' + f'/{str(page)}'
    
    def download_image(self, url: str) -> bytes:
        resp = self._request(requests.get, url, headers=self.headers)
        return resp.content