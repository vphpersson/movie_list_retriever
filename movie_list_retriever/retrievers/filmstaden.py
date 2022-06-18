from typing import Final

from playwright.async_api import Page

from movie_list_retriever.structures import FilmstadenMovieEntry

EXTRACT_IDS_SCRIPT: Final[str] = """
(() => {
    const movie_ids = Array.from(document.querySelectorAll('a.image-url__url.au-target:not(.news-list-full__list-item-url)')).map(a => a.href.match(/^.*(NCG\d+).*$/)[1])
    if (movie_ids.length === 0)
        return false

    return movie_ids;
})();
"""

EXTRACT_MOVIES_SCRIPT: Final[str] = """
f = async movie_ids => {
    const url = new URL('https://www.filmstaden.se/api/v2/movie/en')
    url.searchParams.set('movieNcgIds', movie_ids.join(','))

    return (await (await fetch(url.toString())).json()).items.map(item => {
        return {
            title: item.title,
            directors: item.directors.map(director => director.displayName),
            original_language: item.originalLanguage,
            original_title: item.originalTitle,
            year: item.productionYear,
            release_date: item.releaseDate.replace(/T00:00:00$/, '')
        };
    });
}
"""


async def retrieve_filmstaden_movies(page: Page) -> list[FilmstadenMovieEntry]:
    await page.goto(url='https://www.filmstaden.se/utmarktfilm')
    await page.click(selector='#onetrust-reject-all-handler')
    movie_ids = (await (await page.wait_for_function(EXTRACT_IDS_SCRIPT)).json_value())['_rejectionHandler0']

    return [
        FilmstadenMovieEntry(**movie_dict)
        for movie_dict in await page.evaluate(EXTRACT_MOVIES_SCRIPT, movie_ids)
    ]
