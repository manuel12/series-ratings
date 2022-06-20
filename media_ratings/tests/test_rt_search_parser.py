import validators

from django.test import TestCase
from media_ratings.search_parsers import RottentomatoesSearchResultsParser

class RTSearchParserTests(TestCase):
    def setUp(self):
        search_term = "Breaking Bad"
        
        RottentomatoesSearchResultsParser.search_url_prefix = "https://www.rottentomatoes.com/search?search="
        RottentomatoesSearchResultsParser.search_result_elem_cls = "search-page-media-row"
        self.search_parser = RottentomatoesSearchResultsParser(search_term)

    def test_url(self):
        self.assertEqual(self.search_parser.url,
            "https://www.rottentomatoes.com/search?search=Breaking+Bad")
        
    def test_clean_up_url(self):
        search_term = "Bla bla bla la-da-dee-da-do"
        search_parser = RottentomatoesSearchResultsParser(search_term)
        self.assertEqual(search_parser.url,
                         "https://www.rottentomatoes.com/search?search=Bla+bla+bla+la+da+dee+da+do")

    def test_validate_search_result_text(self):
        search_result_text = self.search_parser.get_first_search_result_text()
        self.assertTrue(
            self.search_parser.validate_search_result_text(search_result_text))

    def test_get_search_results(self):
        search_results = self.search_parser.get_tv_search_results()

        self.assertEqual(str(type(search_results)), "<class 'bs4.element.ResultSet'>")
        self.assertEqual(search_results.__class__.__name__, "ResultSet")
        self.assertEqual(str(type(search_results[0])), "<class 'bs4.element.Tag'>")
        self.assertEqual(search_results[0].__class__.__name__, "Tag")

    def test_get_search_results_urls(self):
        search_result_urls = self.search_parser.get_tv_search_results_urls()
        
        for url in search_result_urls:
            self.assertTrue(validators.url(url))

    def test_get_first_search_result_url(self):
        search_term = "Breaking Bad"
        search_parser = RottentomatoesSearchResultsParser(search_term)
        search_result_urls = search_parser.get_tv_search_results_urls()
        first_search_result_url = search_parser.get_first_tv_search_result_url()
        
        self.assertEqual(first_search_result_url, search_result_urls[0])

    def test_no_results_found(self):
        RottentomatoesSearchResultsParser.search_result_elem_cls = "non-existant-class"
        self.assertTrue(self.search_parser.no_results_found())


    def test_all_words_present_on_text(self):
        search_result_text = self.search_parser.get_first_search_result_text()
        self.assertTrue(self.search_parser.validate_search_result_text(search_result_text))