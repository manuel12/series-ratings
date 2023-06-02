from bs4 import BeautifulSoup
import urllib.request


def clean_up_url(url):
    """
        Returns a clean url string.
        Url before cleaning: https://www.imdb.com/title/love death and-robots/
        Url after cleaning: https://www.imdb.com/title/love+death+and+robots/
        """
    print(f"-- Cleaning url: [ {url} ]...")
    cleaned_url = url.strip().replace(" ", "+").replace("-", "+")
    print(f"-- Cleaned url: [ {cleaned_url} ]...")
    return cleaned_url


def get_page_source(url):
    print(f"-- Opening: [ {url} ]...")
    # It seems like IMDb does not like the user agent of Python 3.x so 403 error is shown.
    # Specifying User-Agent solves the problem.
    req = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req)
    return page.read()


def get_rt_scores(search_query):
    print(f"--- [ GETTING ROTTEN TOMATOES SCORES ] ---")
    # Form rt search results page url
    search_url_prefix = "https://www.rottentomatoes.com/search?search="

    search_url = search_url_prefix + search_query
    search_url = clean_up_url(search_url)

    # Use search url to get the soup of rt search results page
    print(f"-- Getting soup from search url [ {search_url} ]...")
    soup = BeautifulSoup(get_page_source(search_url), 'html.parser')

    # Get tv section if it's present, if it's not return falses
    tv_section = soup.select("[type=tvSeries]")
    tv_section = tv_section[0]

    # Get the search results on the tv section
    tv_section_results = tv_section.select("search-page-media-row")

    # Get first result
    first_result = tv_section_results[0]

    # Get first result url
    result_urls = first_result.select('a[href]')
    result_url = result_urls[0]

    # Get the url for the first url
    first_result_url = result_url.get('href')
    print(f"-- {first_result_url}")

    # Use first_result_url to get a new soup
    new_soup = BeautifulSoup(get_page_source(
        first_result_url), 'html.parser')
    series_score_board = new_soup.select("score-board")[0]

    # Get tomatometer and audience score
    score_board_tomatometer_value = series_score_board.get(
        'tomatometerscore')
    score_board_audience_score_value = series_score_board.get(
        'audiencescore')

    # Get the tomatometer and audience score values from the attributes of the same name
    # on the score board element:
    #   <score-board tomatometerscore=100  audiencescore=97 />

    # In case any of them is not present, or '' None will be set instead.
    tomatometer_score = int(
        score_board_tomatometer_value) if score_board_tomatometer_value else None
    audience_score = int(
        score_board_audience_score_value) if score_board_audience_score_value else None

    print(
        f"-- tomatometer_score: {tomatometer_score} - audience_score: {audience_score}")

    return {
        "tomatometer": tomatometer_score,
        "audience_score": audience_score
    }
