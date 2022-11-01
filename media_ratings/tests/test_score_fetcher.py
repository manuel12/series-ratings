from django.test import TestCase
from media_ratings.models import TV_Series, IMDbScores, RottentomatoesScores
from media_ratings.score_fetcher import ScoreFetcher
from media_ratings.parsers import IMDbMediaPageParser, RottentomatoesMediaPageParser
from media_ratings.search_parsers import IMDBSearchResultsParser, RottentomatoesSearchResultsParser
# Create your tests here.


class ScoreFetcherTests(TestCase):
    def setUp(self):
        print("ScoreFetcherTests")

        search_term = "True Detective"

        self.tv_series = TV_Series.objects.create(title="True Detective")
        self.score_fetcher = ScoreFetcher(search_term)

    def test_get_score_data(self):
        score_data = self.score_fetcher.get_score_data()
        clean_imdb_score = float(score_data["imdb"].split("/")[0])
        self.assertTrue(score_data["imdb"], 0 < clean_imdb_score < 10)

        clean_tomatometer_score = int(
            score_data["rt"]["tomatometer"].replace("%", ""))
        self.assertTrue(0 < clean_tomatometer_score < 101)

        clean_audience_score = int(
            score_data["rt"]["audience_score"].replace("%", ""))
        self.assertTrue(0 < clean_audience_score < 101)

    def test_get_score_data_returns_na_when_imdb_score_not_found(self):
        search_term = "Non Existing Movie"
        score_fetcher = ScoreFetcher(search_term)

        score_data = score_fetcher.get_score_data()
        self.assertEqual(score_data["imdb"], "N/A")

    def test_get_score_data_returns_na_when_rt_score_not_found(self):
        search_term = "Non Existing Movie"
        score_fetcher = ScoreFetcher(search_term)

        score_data = score_fetcher.get_score_data()
        self.assertEqual(score_data["rt"]["tomatometer"], "N/A")
        self.assertEqual(score_data["rt"]["audience_score"], "N/A")

    def test_fetch_score_with_imdb_data(self):
        self.assertTrue(0 < self.score_fetcher.fetch_score(
            "imdb", IMDBSearchResultsParser, IMDbMediaPageParser) < 10)

    def test_fetch_score_returns_none_when_imdb_score_not_found(self):
        search_term = "Non Existing Movie"
        score_fetcher = ScoreFetcher(search_term)
        self.assertEqual(score_fetcher.fetch_score(
            "imdb", IMDBSearchResultsParser, IMDbMediaPageParser), None)

    def test_fetch_score_with_rt_data(self):
        rt_scores = self.score_fetcher.fetch_score(
            "rt", RottentomatoesSearchResultsParser, RottentomatoesMediaPageParser)
        self.assertTrue(0 < rt_scores["tomatometer"] < 101)
        self.assertTrue(0 < rt_scores["audience_score"] < 101)

    def test_fetch_score_returns_none_when_rt_score_not_found(self):
        search_term = "Non Existing Movie"
        score_fetcher = ScoreFetcher(search_term)
        self.assertEqual(score_fetcher.fetch_score(
            "rt", RottentomatoesSearchResultsParser, RottentomatoesMediaPageParser),
            {'tomatometer': None, 'audience_score': None})

    def test_create_imdb_score_model_instance(self):
        imdb_score_value = 8.9

        imdb_score_model_instance = self.score_fetcher.create_score_model_instance(
            IMDbScores,
            media=self.tv_series,
            imdb_score=imdb_score_value)
        self.assertEqual(imdb_score_model_instance.__class__, IMDbScores)

    def test_create_rt_score_model_instance(self):
        tomatometer_value = 78
        audience_score_value = 75

        rt_score_model_instance = self.score_fetcher.create_score_model_instance(
            RottentomatoesScores,
            media=self.tv_series,
            tomatometer_score=tomatometer_value,
            audience_score=audience_score_value)
        self.assertEqual(rt_score_model_instance.__class__,
                         RottentomatoesScores)
