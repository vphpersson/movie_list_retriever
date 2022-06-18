#!/usr/bin/env python

from asyncio import run as asyncio_run
from typing import Type, Any
from dataclasses import is_dataclass, asdict
from sys import stderr
from json import dumps as json_dumps

from playwright.async_api import async_playwright
from httpx import AsyncClient

from movie_list_retriever.cli import MovieListRetrieverArgumentParser, SupportedSource
from movie_list_retriever.structures import FilmstadenMovieEntry, NewYorkTimesMovieEntry
from movie_list_retriever.retrievers.filmstaden import retrieve_filmstaden_movies
from movie_list_retriever.retrievers.new_york_times import retrieve_new_york_times_movies


def _dumps_function(obj: Any):
    if is_dataclass(obj):
        return asdict(obj)

    raise TypeError


async def movie_list_retriever():
    args: Type[MovieListRetrieverArgumentParser.Namespace] = MovieListRetrieverArgumentParser().parse_args()

    match source := args.source:
        case SupportedSource.FILMSTADEN:
            async with async_playwright() as p:
                browser = await p.firefox.launch()
                movie_entries: list[FilmstadenMovieEntry] = await retrieve_filmstaden_movies(
                    page=await browser.new_page()
                )
                await browser.close()
        case SupportedSource.NEW_YORK_TIMES:
            async with AsyncClient() as http_client:
                # TODO: I need to use sub-parser to support provision of arguments per retriever type...
                movie_entries: list[NewYorkTimesMovieEntry] = await retrieve_new_york_times_movies(
                    http_client=http_client,
                    num_calls=1
                )
        case _:
            print(f'Unexpected source: "{source}".', file=stderr)
            exit(1)

    print(json_dumps(movie_entries, default=_dumps_function))


if __name__ == '__main__':
    asyncio_run(movie_list_retriever())
