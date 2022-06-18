from httpx import AsyncClient, Response

from movie_list_retriever.structures import NewYorkTimesMovieEntry


async def retrieve_new_york_times_movies(
    http_client: AsyncClient,
    num_calls: int,
    num_movies_limit: int = 20
) -> list[NewYorkTimesMovieEntry]:

    url_params = {
        'pick': 'y',
        'order': 'publication_date',
        'sort-order': 'desc',
        'limit': str(num_movies_limit)
    }

    entries: list[NewYorkTimesMovieEntry] = []

    for i in range(num_calls):
        url_params['offset'] = str(i * num_movies_limit)

        response: Response = await http_client.get(
            url='https://content.api.nytimes.com/svc/movies/v3/movies.json',
            params=url_params
        )
        response.raise_for_status()

        entries.extend([
            NewYorkTimesMovieEntry(
                title=json_data['title'],
                directors=json_data['directors'] or [],
                year=json_data['year'],
                release_date=json_data['release_date_us'],
                imdb_id=json_data['imdb'],
                review_publish_date=json_data['reviews'][0]['publish_date'],
                review_lead_paragraph=json_data['reviews'][0]['summary'],
                review_link=f"https://www.nytimes.com/{json_data['reviews'][0]['review_url']}"
            )
            for json_data in response.json()['results']
        ])

    return entries
