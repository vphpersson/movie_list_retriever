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
