#!/usr/bin/env python

from asyncio import run as asyncio_run
from typing import Type, Any
from dataclasses import is_dataclass, asdict
from json import dumps as json_dumps

from movie_list_retriever.cli import MovieListRetrieverArgumentParser
from movie_list_retriever import retrieve_movie_entries


def _dumps_function(obj: Any):
    if is_dataclass(obj):
        return asdict(obj)

    raise TypeError


async def movie_list_retriever():
    # TODO: I need to use sub-parser to support provision of arguments per retriever type...
    args: Type[MovieListRetrieverArgumentParser.Namespace] = MovieListRetrieverArgumentParser().parse_args()
    print(json_dumps(await retrieve_movie_entries(source=args.source), default=_dumps_function))


if __name__ == '__main__':
    asyncio_run(movie_list_retriever())
