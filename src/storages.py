from pathlib import Path
import typing as tp
import hashlib
import json
import os

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

    
class ImagesStorage:
    """
    Просто хранилище изображений.
    Сохраняет изображения по заданному пути.
    """

    def save(self, path: tp.Union[str, Path], image_bytes: bytes) -> None:
        with open(path, 'wb') as f:
            f.write(image_bytes)
        

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
        unique_digest = hashlib.blake2s(data.url.encode()).hexdigest()
        filename = f'{data.fullname[:30]}... ({unique_digest}).json'
        filepath = self._root.joinpath(filename)
        return super().save(filepath, data.as_dict())  


class NemezidaImagesStorage(ImagesStorage, SimpleFileStorage):
    """
    Хранилище для изображений с сайта nemez1da.ru с определенной 
    структурой.
    """

    def save(self, image_bytes: bytes, url: str) -> None:
        unique_digest = hashlib.blake2s(url.encode()).hexdigest()
        filename = f'{unique_digest}.jpg'
        filepath = self._root.joinpath(filename)
        super().save(filepath, image_bytes)
        return filename
