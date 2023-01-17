from threading import current_thread
import requests


def before_request(method: str, url: str, current_retry_num: int, retries: int):
    print(f'{current_thread().name}\tREQ\t{method.upper()} [{current_retry_num}/{retries}] {url}')


def after_request(method: str, url: str, current_retry_num: int, retries: int, response: requests.Response):
    print(f'{current_thread().name}\t{response.status_code}\t{method.upper()} [{current_retry_num}/{retries}] {url}')


def on_request_exception(method: str, url: str, current_retry_num: int, retries: int, ex: Exception):
    type = 'ERR' if current_retry_num == retries else 'WAR'
    print(f'{current_thread().name}\t{type}\t{method.upper()} [{current_retry_num}/{retries}] {url}\n{ex}')

