from dataclasses import dataclass
from typing import List


@dataclass
class NewsTagDTO:
    titleTag: str
    slagTag: str

@dataclass
class NewsCategoryDTO:
    titleCategory: str
    slagCategory: str
    contentCategory: str

@dataclass
class FormsnewsDTO:
    nameComm: str
    emailComm: str
    textComm: str
    time_create: str

@dataclass
class NewsDTO:
    imgnews: str
    dataNews: str
    titlenews: str
    slugnews: str
    contentnews: str
    tags: List[NewsTagDTO]
    category: NewsCategoryDTO