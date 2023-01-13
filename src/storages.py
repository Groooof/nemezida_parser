from pathlib import Path
import typing as tp
from random import randint
import os
import datetime as dt
import json


class SimpleFileStorage:
    def __init__(self, path: tp.Union[str, Path]) -> None:
        self.path = Path(path)
        self._create_folder(path)
        
    def _create_folder(self, path: tp.Union[str, Path]) -> None:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
    
        
class ImagesStorage(SimpleFileStorage):
        
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
    
    def save(self, data: tp.Union[dict, tp.List[dict]]) -> None:
        current_datetime = dt.datetime.now().strftime('%Y.%m.%d %H:%M:%S.%f')
        filename = f'{current_datetime}.json'
        filepath = self.path.joinpath(filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)