from dataclasses import (
    dataclass,
    asdict
)
import typing as tp


@dataclass
class BaseDataclass:
    def as_dict(self):
        return asdict(self)


@dataclass
class BaseCardData(BaseDataclass):
    fullname: str
    date: str
    category: str
    info: dict
    url: str


@dataclass
class ParsedCardData(BaseCardData):
    photos_urls: tp.List[str]
    

@dataclass
class CardDataForSave(BaseCardData):
    photos_ids: tp.List[int]