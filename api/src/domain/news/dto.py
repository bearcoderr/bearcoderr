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
    post_id: int
    imgnews: str
    dataNews: str
    titlenews: str
    slugnews: str
    contentnews: str
    tags: List[NewsTagDTO]
    category: NewsCategoryDTO


@dataclass
class CommentDTO:
    nameComm: str
    emailComm: str
    textComm: str
    time_create: str
    post_id: int


@dataclass
class FeedDTO:
    imgnews: str
    titlenews: str
    slugnews: str
    contentnews: str
    text_twitter: str
    feed_or_not: bool
