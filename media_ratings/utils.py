import urllib.request
import json


def load_json_data(file):
    with open(file) as f:
        data = json.load(f)
    return data


def save_json_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)


def capitalize_phrase(phrase=""):
    """Capitalizes all words in a phrase."""
    raise_attribute_error_if_missing(phrase)
    return " ".join([word.capitalize() for word in phrase.split(" ")])


def sanitize_phrase(phrase=""):
    """Converts '&'s to 'and's and hyphens to spaces."""
    raise_attribute_error_if_missing(phrase)
    return "".join(char.replace("&", "and").replace("-", " ") for char in phrase)


def standardize_phrase(phrase=""):
    """Capitalizes and sanitizes phrases."""
    return capitalize_phrase(sanitize_phrase(phrase))


def raise_attribute_error_if_missing(phrase=None):
    """Raises error if phrase is missing or falsey."""
    if not phrase:
        raise AttributeError("The search term cannot be empty.")


def add_pluses_to_url(url):
    """
    Returns a string url with spaces replaced with pluses.
    Url before: https://www.imdb.com/title/love death and-robots/
    Url after: https://www.imdb.com/title/love+death+and+robots/
    """
    print(f"-- Adding pluses url: [ {url} ]...")
    updated_url = url.strip().replace(" ", "+").replace("-", "+")
    print(f"-- Cleaned url: [ {updated_url} ]...")
    return updated_url


def get_page_source(url):
    """
    Returns the html  source of the page.
    """
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
