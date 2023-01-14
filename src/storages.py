from random import randint
from pathlib import Path
import datetime as dt
import typing as tp
import json
import os
from urllib.parse import urlparse

from . import dto


class SimpleFileStorage:
    """
    Базовый класс для простого хранилища файлов.
    Создает корневую папку по указанному пути для 
    дальнейшего хранения файлов в ней.
    """
    def __init__(self, root: tp.Union[str, Path]) -> None:
        self._root = Path(root)
        self._create_folder(root)
        
    def _create_folder(self, path: tp.Union[str, Path]) -> None:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        
class ImagesStorage(SimpleFileStorage):
    """
    Простое хранилище изображений.
    Каждому изображению присваивается id, которое 
    является именем файла.
    Сохраняет с расширением .jpg.
    """
        
    def save(self, bytes_data: bytes) -> int:
        id = self._generate_id()
        filename = f'{str(id)}.jpg'
        filepath = self._root.joinpath(filename)
        
        with open(filepath, 'wb') as f:
            f.write(bytes_data)
        return id
    
    @staticmethod
    def _generate_id() -> int:
        return randint(1, 99999)
        
        
class JsonStorage:
    """
    Просто хранилище файлов json.
    Сохраняет файлы в формате json по заданному пути.
    """
      
    def save(self, path: tp.Union[str, Path], data: tp.Union[dict, tp.List[dict]]) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            

class NemezidaJsonStorage(JsonStorage, SimpleFileStorage):
    """
    Хранилище для карточек с сайта nemez1da.ru в формате json и
    с определенной структурой.
    """
    
    def save(self, data: dto.CardDataForSave) -> None:
        prepared_url = '-'.join(urlparse(data.url).path.strip('/').split('/'))
        filename = f'{data.fullname}_{prepared_url}.json'
        filepath = self._root.joinpath(filename)
        return super().save(filepath, data.as_dict())  
