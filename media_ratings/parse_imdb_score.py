from bs4 import BeautifulSoup
from utils import add_pluses_to_url, get_page_source


def get_imdb_score(search_query):
    print(f"--- [ GETTING IMDB SCORE ] ---")
    # Forms an imdb search results page url by appending imdb url prefix, search query and suffix
    search_url_prefix = "https://www.imdb.com/search/title/?title="
    search_url_suffix = "&languages=en"

    imdb_search_results_url = add_pluses_to_url(
        search_url_prefix + search_query + search_url_suffix)

    # Use imdb search results page url to get the soup representation of imdb search results page
    print(
        f"-- Getting soup from search results page url [ {imdb_search_results_url} ]...")
    search_results_page_soup = BeautifulSoup(get_page_source(
        imdb_search_results_url), 'html.parser')

    # Get first 3 search results elements
    search_result_elem_class = "mode-advanced"
    search_result_elems = search_results_page_soup.find_all(
        class_=search_result_elem_class, limit=3)

    # Of these 3 search result elements add the ones that are tv series to the search results tv series array

    # A tv series is defined as:
    #   1) A result element that has a class '.certificate' that contains the text 'TV-', as in  'TV-MA', for example
    #   2) A result element that has NO 'Gross:' text, as in 'Gross: $253.00M' (reserved for movies)
    #   3) A result element that has a class '.genre' and contains NO "Documentary" text (reserved for movies)

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

    # EXPLANATION: Generally if there's more than 1 match (if there exists the original series
    #   plus remakes), or in general if is more than 1 result in IMDb's tv section
    #   generally the results with the highest score is the original series
    #   (not an exact science...)

    # If there is only 1 search_result_tv_series, make that one the correct search result element
    if len(search_result_tv_series) == 0:
        correct_search_result_elem = search_result_tv_series[0]

    # Else pick the search result tv series  with the highest score
    else:
        search_result_tv_series_scores = [
            float(series.find("strong").text) for series in search_result_tv_series]
        max_tv_series_score = max(search_result_tv_series_scores)
        max_tv_series_score_index = search_result_tv_series_scores.index(
            max_tv_series_score)
        max_score_tv_series = search_result_tv_series[max_tv_series_score_index]
        correct_search_result_elem = max_score_tv_series

    # Return correct search result element score element text
    imdb_score_text = correct_search_result_elem.find("strong").text

    # Make score text into a float
    imdb_score = float(imdb_score_text)

    print(
        f"-- imdb_score for '{search_query}': {imdb_score}")

    return imdb_score
