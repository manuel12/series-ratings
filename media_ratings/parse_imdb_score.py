from bs4 import BeautifulSoup
import urllib.request

# -Write a story about a developer who pitches a lead developer position
#   leads his team to great successes and by night enjoys the polish
#   nightlife and hooking up  with girls.


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
        url, headers={
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0'
        })
    page = urllib.request.urlopen(req)
    return page.read()


def get_imdb_score(search_query):
    print(f"--- [ GETTING IMDB SCORE ] ---")
    # Form imdb search results page url by adding the search query equal to the title param
    search_url_prefix = "https://www.imdb.com/search/title/?title="
    search_url_suffix = "&languages=en"

    search_url = search_url_prefix + search_query + search_url_suffix
    search_url = clean_up_url(search_url)

    # Use search url to get the soup of imdb search results page
    print(f"-- Getting soup from search url [ {search_url} ]...")
    soup = BeautifulSoup(get_page_source(search_url), 'html.parser')

    # Get first 3 search results.
    search_result_elems = soup.find_all(
        class_="mode-advanced", limit=3)

    # Get first 3 search results that are tv series
    #   Define a tv series as:
    #   1) A result element ."mode-advanced" that has a .certificate with text 'TV-'
    #   2) A result element ."mode-advanced" that has NO "Gross:" text
    #   3) A result element ."mode-advanced" that has NO "Documentary" text

    search_result_tv_series = []
    for elem in search_result_elems:
        series_certificate_elem = elem.find(class_="certificate")
        series_certificate_text = series_certificate_elem.text if series_certificate_elem else None

        genre_elem = elem.find(class_="genre")
        genre_elem_text = genre_elem.text if genre_elem else None

        gross_revenue_text = elem.find(string="Gross:")

        if series_certificate_text and "TV-" in series_certificate_text and genre_elem_text and "Documentary" not in genre_elem_text and gross_revenue_text is None:
            search_result_tv_series.append(elem)

    # Of the tv series search results return the one with the highest score
    # EXPLANATION:
    #   Generally if there's more than 1 match(if there exists the original series)
    #   plus remakes, or in general if is more than 1 result in IMDb's tv section
    #   generally the results with the highest score is the original series
    #   (not an exact science...)

    # If there is only 1 search_result_tv_series, make that one the correct_search_result_elem
    if len(search_result_tv_series) == 0:
        correct_search_result_elem = search_result_tv_series[0]
    # Else pick the search_result_tv_series with the highest score
    else:
        search_result_tv_series_scores = [
            float(series.find("strong").text) for series in search_result_tv_series]
        max_tv_series_score = max(search_result_tv_series_scores)
        max_tv_series_score_index = search_result_tv_series_scores.index(
            max_tv_series_score)
        max_score_tv_series = search_result_tv_series[max_tv_series_score_index]
        correct_search_result_elem = max_score_tv_series

    # Return correct_search_result_elem score element text
    imdb_score_text = correct_search_result_elem.find("strong").text

    # Make score text into a float
    imdb_score = float(imdb_score_text)

    print(
        f"-- imdb_score for '{search_query}': {imdb_score}")

    return imdb_score


# get_imdb_score("The a team")
