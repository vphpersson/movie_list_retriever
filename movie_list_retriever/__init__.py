from enum import Enum

from playwright.async_api import async_playwright
from httpx import AsyncClient

from movie_list_retriever.structures import MovieEntry, FilmstadenMovieEntry, NewYorkTimesMovieEntry
from movie_list_retriever.retrievers.filmstaden import retrieve_filmstaden_movies
from movie_list_retriever.retrievers.new_york_times import retrieve_new_york_times_movies


class SupportedSource(Enum):
    NEW_YORK_TIMES = 'new_york_times'
    FILMSTADEN = 'filmstaden'

    def __str__(self) -> str:
        return self.value


async def retrieve_movie_entries(source: SupportedSource) -> list[MovieEntry]:
    match source:
        case SupportedSource.FILMSTADEN:
            async with async_playwright() as p:
                browser = await p.firefox.launch()
                movie_entries: list[FilmstadenMovieEntry] = await retrieve_filmstaden_movies(
                    page=await browser.new_page()
                )
                await browser.close()
        case SupportedSource.NEW_YORK_TIMES:
            async with AsyncClient() as http_client:
                movie_entries: list[NewYorkTimesMovieEntry] = await retrieve_new_york_times_movies(
                    http_client=http_client,
                    num_calls=1
                )
        case _:
            raise ValueError(f'Unexpected source: "{source}".')

    return movie_entries
