from importlib import resources as importlib_resources

from playwright.async_api import Page

from movie_list_retriever.structures import FilmstadenMovieEntry


async def retrieve_filmstaden_movies(page: Page) -> list[FilmstadenMovieEntry]:
    extract_ids_script = importlib_resources.read_text(
        package='movie_list_retriever.retrievers.filmstaden',
        resource='extract_ids.js'
    )

    extract_movies_script = importlib_resources.read_text(
        package='movie_list_retriever.retrievers.filmstaden',
        resource='extract_movies.js'
    )

    await page.goto(url='https://www.filmstaden.se/utmarktfilm')
    await page.click(selector='#onetrust-reject-all-handler')
    movie_ids = (await (await page.wait_for_function(extract_ids_script)).json_value())['_rejectionHandler0']

    return [
        FilmstadenMovieEntry(**movie_dict)
        for movie_dict in await page.evaluate(extract_movies_script, movie_ids)
    ]
