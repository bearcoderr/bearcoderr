from dataclasses import dataclass
from datetime import date


@dataclass
class PagesDTO:
    id: int
    title: str
    slug: str
    content: str
    publication_date: date
    last_updated: date
