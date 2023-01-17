import typing as tp
from time import sleep
from math import sqrt
import requests


class RequestsEngine:
    def __init__(self, 
                 default_timeout: int = 3, 
                 default_retries: int = 3, 
                 before_request: tp.Callable = lambda: None,
                 after_request: tp.Callable = lambda: None,
                 on_exception: tp.Callable = lambda: None) -> None:
        self._default_timeout = default_timeout
        self._default_retries = default_retries
        self._before_request = before_request
        self._after_request = after_request
        self._on_exception = on_exception
    
    def request(self, 
                method: tp.Callable, 
                url: str, 
                timeout: tp.Optional[int] = None, 
                retries: tp.Optional[int] = None, 
                **kwargs) -> requests.Response:
        
        timeout = self._default_timeout if timeout is None else timeout
        retries = self._default_retries if retries is None else retries
        
        for current_retry_num in range(1, retries+1):

            try:
                self._before_request(method.__name__, url, current_retry_num, retries)
                resp = method(url, timeout=timeout, **kwargs)
                resp.raise_for_status()
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as ex:
                self._on_exception(method.__name__, url, current_retry_num, retries, ex)
                self._raise_for_retry(current_retry_num, retries)
                self._sleep(current_retry_num)
            else:
                self._after_request(method.__name__, url, current_retry_num, retries, resp)
                return resp
                
    @staticmethod
    def _raise_for_retry(current_retry: int, retries: int) -> None:
        if current_retry == retries:
            raise
        
    @staticmethod
    def _sleep(current_retry: int) -> None:
        sleep(round(sqrt(current_retry*2), 2))
