from django.test import TestCase
from media_ratings.models import TV_Series, IMDbScores, RottentomatoesScores
from media_ratings.score_manager import ScoreManager
from media_ratings.parsers import IMDbMediaPageParser, RottentomatoesMediaPageParser
from media_ratings.search_parsers import IMDBSearchResultsParser, RottentomatoesSearchResultsParser
# Create your tests here.


class ScoreManagerTests(TestCase):
    def setUp(self):
        search_term = "True Detective"

        self.tv_series = TV_Series.objects.create(title="True Detective")
        self.score_manager = ScoreManager(search_term)

    def test_get_score_data(self):
        score_data = self.score_manager.get_score_data()
        self.assertEqual(score_data["imdb"], "8.9/10")
        self.assertEqual(score_data["rt"]["tomatometer"], "78%")
        self.assertEqual(score_data["rt"]["audience_score"], "74%")

    def test_get_score_data_returns_na_when_imdb_score_not_found(self):
        search_term = "Non Existing Movie"
        score_manager = ScoreManager(search_term)

        score_data = score_manager.get_score_data()
        self.assertEqual(score_data["imdb"], "N/A")

    def test_get_score_data_returns_na_when_rt_score_not_found(self):
        search_term = "Non Existing Movie"
        score_manager = ScoreManager(search_term)

        score_data = score_manager.get_score_data()
        self.assertEqual(score_data["rt"]["tomatometer"], "N/A")
        self.assertEqual(score_data["rt"]["audience_score"], "N/A")

    def test_fetch_score_with_imdb_data(self):
        self.assertEqual(self.score_manager.fetch_score("imdb", IMDBSearchResultsParser, IMDbMediaPageParser), 8.9)

    def test_fetch_score_returns_none_when_imdb_score_not_found(self):
        search_term = "Non Existing Movie"
        score_manager = ScoreManager(search_term)
        self.assertEqual(score_manager.fetch_score("imdb", IMDBSearchResultsParser, IMDbMediaPageParser), None)

    def test_fetch_score_with_rt_data(self):
        rt_scores = self.score_manager.fetch_score("rt", RottentomatoesSearchResultsParser, RottentomatoesMediaPageParser)
        self.assertEqual(rt_scores["tomatometer"], 78)
        self.assertEqual(rt_scores["audience_score"], 74)

    def test_fetch_score_returns_none_when_rt_score_not_found(self):
        search_term = "Non Existing Movie"
        score_manager = ScoreManager(search_term)
        self.assertEqual(score_manager.fetch_score("rt", RottentomatoesSearchResultsParser, RottentomatoesMediaPageParser), None)

    def test_create_imdb_score_model_instance(self):
        imdb_score_value = 8.9

        imdb_score_model_instance = self.score_manager.create_score_model_instance(
            IMDbScores,
            media=self.tv_series,
            imdb_score=imdb_score_value)
        self.assertEqual(imdb_score_model_instance.__class__, IMDbScores)

    def test_create_rt_score_model_instance(self):
        tomatometer_value = 78
        audience_score_value = 75

        rt_score_model_instance = self.score_manager.create_score_model_instance(
            RottentomatoesScores,
            media=self.tv_series,
            tomatometer_score=tomatometer_value,
            audience_score=audience_score_value)
        self.assertEqual(rt_score_model_instance.__class__,
                         RottentomatoesScores)
