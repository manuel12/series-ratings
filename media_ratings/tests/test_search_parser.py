import validators

from django.test import TestCase
from media_ratings.search_parsers import SearchResultsParser

html_page = """
<html>
    <head><title>Mock Page</title></head>
    <body>
        <div class="search-results-wrapper">
            <div class="search-result">
                <a href="/breaking-bad">Breaking Bad</a>
            </div>
            <div class="search-result">
                <a href="/the-wire">The Wire</a>
            </div>
            <div class="search-result">
                <a href="/the-sopranos">The Sopranos</a>
            </div>
            <div class="search-result">
                <a href="/six-feet-under">Six Feet Under</a>
            </div>
        </div
    </body>
</html>
"""


class SearchResultsParserTests(TestCase):
    def setUp(self):
        search_term = "Breaking Bad"
        SearchResultsParser.search_url_prefix = "https://duckduckgo.com/?q="
        SearchResultsParser.search_url_suffix = "&t=h_&ia=web"
        SearchResultsParser.search_result_elem_cls = "search-result"
        
        self.search_parser = SearchResultsParser(search_term, html_page)

    def test_url(self):
        self.assertEqual(self.search_parser.url,
                         "https://duckduckgo.com/?q=Breaking+Bad&t=h_&ia=web")

    def test_clean_up_url(self):
        search_term = "Bla bla bla la-da-dee-da-do"
        search_parser = SearchResultsParser(search_term)
        self.assertEqual(search_parser.url,
                         "https://duckduckgo.com/?q=Bla+bla+bla+la+da+dee+da+do&t=h_&ia=web")

    def test_validate_search_result_text(self):
        search_result_text = self.search_parser.get_first_search_result_text()
        print(search_result_text)
        self.assertTrue(
            self.search_parser.validate_search_result_text(search_result_text))

    def test_get_search_results(self):
        search_results = self.search_parser.get_search_results()

        self.assertEqual(str(type(search_results)), "<class 'bs4.element.ResultSet'>")
        self.assertEqual(search_results.__class__.__name__, "ResultSet")
        self.assertEqual(str(type(search_results[0])), "<class 'bs4.element.Tag'>")
        self.assertEqual(search_results[0].__class__.__name__, "Tag")

    def test_get_search_urls(self):
        search_result_urls = self.search_parser.get_search_urls()
        for url in search_result_urls:
            self.assertTrue(validators.url(f'https://www.google.com{url}'))

    def test_get_first_search_result_url(self):
        search_result_urls = self.search_parser.get_search_urls()
        first_search_result_url = self.search_parser.get_first_search_result_url()
        self.assertEqual(first_search_result_url, search_result_urls[0])

    def test_no_results_found(self):
        SearchResultsParser.search_result_elem_cls = "non-existant-class"
        self.assertTrue(self.search_parser.no_results_found())

    def test_all_words_present_on_text(self):
        search_result_text = self.search_parser.get_first_search_result_text()
        self.assertTrue(self.search_parser.validate_search_result_text(search_result_text))



