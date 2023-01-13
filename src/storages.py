from random import randint
from pathlib import Path
import datetime as dt
import typing as tp
import json
import os


class SimpleFileStorage:
    """
    Базовый класс для простого хранилища файлов.
    Создает папку по указанному пути для 
    дальнейшего хранения файлов в ней.
    """
    def __init__(self, path: tp.Union[str, Path]) -> None:
        self.path = Path(path)
        self._create_folder(path)
        
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
        filepath = self.path.joinpath(filename)
        
        with open(filepath, 'wb') as f:
            f.write(bytes_data)
        return id
    
    @staticmethod
    def _generate_id() -> int:
        return randint(1, 99999)
        
        
class JsonStorage(SimpleFileStorage):
    """
    Просто хранилище файлов json.
    При сохранении файл именуется текущей датой и временем.
    """
    
    def save(self, data: tp.Union[dict, tp.List[dict]]) -> None:
        current_datetime = dt.datetime.now().strftime('%Y.%m.%d %H:%M:%S.%f')
        filename = f'{current_datetime}.json'
        filepath = self.path.joinpath(filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)