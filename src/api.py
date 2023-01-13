from time import sleep
import typing as tp 
import requests


class BaseApi:
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.838 Yowser/2.5 Safari/537.36'}

    def _request(self, method, url: str, retry: int = 1, **kwargs) -> requests.Response:
        for i in range(1, retry+1):
            try:
                resp = method(url, timeout=3, **kwargs)
                resp.raise_for_status()
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                if i == retry:
                    raise
                sleep(1)
                print(f'Retry #{i}')
            else:
                return resp
            


class NemezidaApi(BaseApi):
    main_url = 'https://nemez1da.ru'
    
    def get_search_page(self, page: tp.Union[str, int] = 1) -> str:
        url = self.generate_search_page_url(page)
        resp = self._request(requests.get, url, retry=3, headers=self.headers)
        return resp.text
    
    def get_card_page(self, url: str) -> str:
        resp = self._request(requests.get, url, retry=3, headers=self.headers)
        return resp.text
    
    def get_image(self, url: str) -> bytes:
        resp = self._request(requests.get, url, retry=3, headers=self.headers)
        return resp.content
    
    def generate_search_page_url(self, page: tp.Union[int, str]) -> str:
        return self.main_url + '/page' + f'/{str(page)}'