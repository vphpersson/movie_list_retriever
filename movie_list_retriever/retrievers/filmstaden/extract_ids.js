(() => {
    const movie_ids = Array.from(document.querySelectorAll('a.image-url__url.au-target:not(.news-list-full__list-item-url)')).map(a => a.href.match(/^.*(NCG\d+).*$/)[1])
    if (movie_ids.length === 0)
        return false

    return movie_ids;
})();
