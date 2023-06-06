from bs4 import BeautifulSoup
from utils import add_pluses_to_url, get_page_source


def get_rt_scores(search_query):
    print(f"--- [ GETTING ROTTEN TOMATOES SCORES ] ---")
    # Form rt search results page url
    search_url_prefix = "https://www.rottentomatoes.com/search?search="
    rt_search_results_url = add_pluses_to_url(search_url_prefix + search_query)

    # Use rt search results page url to get the soup representation of rt search results page
    print(
        f"-- Getting soup from search results page url [ {rt_search_results_url} ]...")
    search_results_page_soup = BeautifulSoup(
        get_page_source(rt_search_results_url), 'html.parser')

    # Get tv section if it's present, if it's not return false
    search_results_tv_section = search_results_page_soup.select(
        "[type=tvSeries]")

    # Since soup.select returns an array get the first item of such array
    # which is also the search results tv section
    search_results_tv_section = search_results_tv_section[0]

    # Get the search results elements on the tv section
    tv_section_results_elems = search_results_tv_section.select(
        "search-page-media-row")

    # Get first result element
    #first_result_elem = tv_section_results_elems[0]
    # =============================================================

    # 1) Get the first 4 search result elements...
    # 2) Iterate through each...
    # 3) Check their score-icon-critic elem...
    # 4) Get their tomatometerscore number...
    # 5) Get their tomatometerstate number...
    # 6) If both are present add them to the correct_results array.

    correct_results = []
    for result_elem in tv_section_results_elems:
        tomatometerscore = result_elem.get('tomatometerscore')
        tomatometerstate = result_elem.get('tomatometerstate')
        print(tomatometerscore, tomatometerstate)
        if tomatometerscore and tomatometerstate:
            correct_results.append(result_elem)

    print(f"-- correct_results: {correct_results}")

    # 1) Iterate throught the correct_results array...
    # 2) Get the max tomatometer score from the array...
    # 3) correct_result_elem is the result with the max tomatometer score...

    max_tomatometer_score = max([int(result.get(
        'tomatometerscore')) for result in correct_results])

    print(f"-- max_tomatometer_score: {max_tomatometer_score}")
    for result in correct_results:
        if max_tomatometer_score == int(result.get('tomatometerscore')):
            correct_result_elem = result

    # =============================================================

    # Get the url for the correct search result
    correct_result_url = correct_result_elem.find('a').get('href')
    print(f"-- {correct_result_url}")

    # Use first_result_url to get a new soup
    new_soup = BeautifulSoup(get_page_source(
        correct_result_url), 'html.parser')
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
