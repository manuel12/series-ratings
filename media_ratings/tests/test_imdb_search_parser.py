import validators

from django.test import TestCase
from media_ratings.search_parsers import IMDBSearchResultsParser


class IMDBSearchParserTests(TestCase):
    def setUp(self):
        search_term = "Breaking Bad"
        
        IMDBSearchResultsParser.search_url_prefix = "https://www.imdb.com/search/title/?title="
        IMDBSearchResultsParser.search_url_suffix = "&languages=en"
        IMDBSearchResultsParser.search_result_elem_cls = "lister-item-header"
        self.search_parser = IMDBSearchResultsParser(search_term)

    def test_url(self):
        self.assertEqual(self.search_parser.url,
                         "https://www.imdb.com/search/title/?title=Breaking+Bad&languages=en")

    def test_clean_up_url(self):
        search_term = "Bla bla bla la-da-dee-da-do"
        search_parser = IMDBSearchResultsParser(search_term)
        self.assertEqual(search_parser.url,
                         "https://www.imdb.com/search/title/?title=Bla+bla+bla+la+da+dee+da+do&languages=en")

    def test_validate_search_result_text(self):
        search_result_text = self.search_parser.get_first_search_result_text()
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
            self.assertTrue(validators.url(f'https://www.imdb.com{url}'))

    def test_get_first_search_result_url(self):
        search_term = "Breaking Bad"
        search_parser = IMDBSearchResultsParser(search_term)
        search_result_urls = search_parser.get_search_urls()
        first_search_result_url = search_parser.get_first_search_result_url()
        
        self.assertEqual(first_search_result_url, f"https://www.imdb.com{search_result_urls[0]}")

    def test_no_results_found(self):
        IMDBSearchResultsParser.search_result_elem_cls = "non-existant-class"
        self.assertTrue(self.search_parser.no_results_found())

    def test_all_words_present_on_text(self):
        search_result_text = self.search_parser.get_first_search_result_text()
        self.assertTrue(self.search_parser.validate_search_result_text(search_result_text))
