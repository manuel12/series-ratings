import validators

from django.test import TestCase
from media_ratings.search_parsers import RottentomatoesSearchResultsParser


class RTSearchParserTests(TestCase):
    def setUp(self):
        search_term = "Breaking Bad"

        RottentomatoesSearchResultsParser.search_url_prefix = "https://www.rottentomatoes.com/search?search="
        RottentomatoesSearchResultsParser.search_result_elem_cls = "search-page-media-row"
        self.search_parser = RottentomatoesSearchResultsParser(search_term)

    def test_url_is_formed_correctly(self):
        self.assertEqual(self.search_parser.url,
                         "https://www.rottentomatoes.com/search?search=Breaking+Bad")

    def test_clean_up_url(self):
        search_term = "Bla bla bla la-da-dee-da-do"
        search_parser = RottentomatoesSearchResultsParser(search_term)
        self.assertEqual(search_parser.url,
                         "https://www.rottentomatoes.com/search?search=Bla+bla+bla+la+da+dee+da+do")

    def test_get_tv_search_result_section_returns_element(self):
        search_result_section = self.search_parser.get_tv_search_results_section()
        self.assertIn('type="tv"', str(search_result_section))

    def test_get_search_results_returns_result_set(self):
        search_results = self.search_parser.get_search_results()

        self.assertEqual(str(type(search_results)),
                         "<class 'bs4.element.ResultSet'>")
        self.assertEqual(search_results.__class__.__name__, "ResultSet")
        self.assertEqual(
            str(type(search_results[0])), "<class 'bs4.element.Tag'>")
        self.assertEqual(search_results[0].__class__.__name__, "Tag")

    def test_get_search_results_returns_empty_result_set_when_no_element_found(self):
        search_term = "Breaking Anatomy"
        RottentomatoesSearchResultsParser.search_result_elem_cls = "non-existant-class"

        search_parser = RottentomatoesSearchResultsParser(search_term)
        search_results = search_parser.get_search_results()

        self.assertEqual(search_results.__class__.__name__, "ResultSet")
        self.assertEqual(search_results, [])

    def test_get_tv_search_urls_returns_urls(self):
        search_result_urls = self.search_parser.get_search_urls()
        for url in search_result_urls:
            self.assertTrue(validators.url(url))

    def test_get_tv_search_urls_returns_none_when_no_elements_found(self):
        search_result_urls = self.search_parser.get_search_urls()
        for url in search_result_urls:
            self.assertTrue(validators.url(url))

    def test_get_first_search_result_url(self):
        search_result_urls = self.search_parser.get_search_urls()
        first_search_result_url = self.search_parser.get_first_search_result_url()

        self.assertEqual(first_search_result_url, search_result_urls[0])

    def test_get_first_search_result_url_returns_none_when_no_element_found(self):
        search_term = "Breaking Bad"
        RottentomatoesSearchResultsParser.search_result_elem_cls = "non-existant-class"

        search_parser = RottentomatoesSearchResultsParser(search_term)
        first_search_result_url = search_parser.get_first_search_result_url()

        self.assertEqual(first_search_result_url, None)

    def test_get_first_search_result_text(self):
        self.assertEqual(
            self.search_parser.get_first_search_result_text(), "Breaking Bad")

    def test_get_first_search_result_text_returns_none_when_no_element_found(self):
        search_term = "Breaking Bad"
        RottentomatoesSearchResultsParser.search_result_elem_cls = "non-existant-class"

        search_parser = RottentomatoesSearchResultsParser(search_term)
        search_result_text = search_parser.get_first_search_result_text()

        self.assertEqual(search_result_text, None)

    def test_get_search_result_url(self):
        self.assertEqual(self.search_parser.get_search_result_url(),
                         "https://www.rottentomatoes.com/tv/breaking_bad")

    def test_get_search_result_url_returns_none_when_no_elements_found(self):
        search_term = "Breaking Bad"
        RottentomatoesSearchResultsParser.search_result_elem_cls = "non-existant-class"

        search_parser = RottentomatoesSearchResultsParser(search_term)
        self.assertEqual(search_parser.get_search_result_url(), None)

    def test_no_results_found(self):
        RottentomatoesSearchResultsParser.search_result_elem_cls = "non-existant-class"
        self.assertTrue(self.search_parser.no_results_found())

    def test_no_results_found_returns_false_when_search_results_are_found(self):
        self.assertFalse(self.search_parser.no_results_found())