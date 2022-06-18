from dataclasses import dataclass
from abc import ABC
from typing import Optional


@dataclass
class MovieEntry(ABC):
    title: str
    directors: list[str]
    year: int
    release_date: Optional[str]


@dataclass
class FilmstadenMovieEntry(MovieEntry):
    original_language: str
    original_title: str


@dataclass
class NewYorkTimesMovieEntry(MovieEntry):
    imdb_id: Optional[str]
    review_publish_date: str
    review_lead_paragraph: str
    review_link: str
