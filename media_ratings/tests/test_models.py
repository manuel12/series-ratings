from django.test import TestCase
from django.db.utils import IntegrityError
from media_ratings.models import TV_Series, IMDbScores, RottentomatoesScores


class TV_SeriesTests(TestCase):
    def setUp(self):
        self.tv_series = TV_Series.objects.create(title="True Detective")

    def test_title_max_length(self):
        tv_series_title_max_length = self.tv_series._meta.get_field(
            "title").max_length
        self.assertEqual(tv_series_title_max_length, 100)

    def test_title_unique(self):
        with self.assertRaises(IntegrityError):
            second_tv_series_with_same_title = TV_Series.objects.create(
                title="True Detective")

    def test_title_blank_false(self):
        tv_series_title_blank = self.tv_series._meta.get_field(
            "title").blank
        self.assertEqual(tv_series_title_blank, False)

    def test_title_null_false(self):
        tv_series_title_null = self.tv_series._meta.get_field(
            "title").null
        self.assertEqual(tv_series_title_null, False)

    def test_description_blank_true(self):
        tv_series_description_blank = self.tv_series._meta.get_field(
            "description").blank
        self.assertEqual(tv_series_description_blank, True)

    def test_imdb_scores_return_value(self):
        IMDbScores.objects.create(media=self.tv_series, imdb_score=8.6)
        imdb_scores = self.tv_series.imdb_scores()
        self.assertEqual(imdb_scores, {'imdb_score': '8.6/10'})

    def test_rt_scores_return_value(self):
        RottentomatoesScores.objects.create(
            media=self.tv_series, tomatometer_score=96, audience_score=94)
        rt_scores = self.tv_series.rottentomatoes_scores()
        self.assertEqual(
            rt_scores, {'tomatometer': '96%', 'audience_score': '94%'})

    def test_imdb_scores_return_value_returns_na_when_no_score_present(self):
        imdb_scores = self.tv_series.imdb_scores()
        self.assertEqual(imdb_scores, {'imdb_score': 'N/A'})

    def test_rottentomatoes_scores_return_na_when_no_score_present(self):
        rt_scores = self.tv_series.rottentomatoes_scores()
        self.assertEqual(
            rt_scores, {'tomatometer': 'N/A', 'audience_score': 'N/A'})


class IMDbScoresTests(TestCase):
    def setUp(self):
        self.tv_series = TV_Series.objects.create(title="True Detective")
        self.imdb_score = IMDbScores.objects.create(
            media=self.tv_series, imdb_score=8.6)

    def test_imdb_score_null_true(self):
        imdb_score_null = self.imdb_score._meta.get_field(
            "imdb_score").null
        self.assertEqual(imdb_score_null, True)

    def test_get_formatted_scores(self):
        formatted_scores = self.imdb_score.get_formatted_scores()
        self.assertEqual(formatted_scores, {'imdb_score': '8.6/10'})

    def test_get_formatted_scores_returns_na_when_score_values_is_null(self):
        tv_series = TV_Series.objects.create(title="Breaking Bad")
        imdb_score = IMDbScores.objects.create(media=tv_series)
        formatted_scores = imdb_score.get_formatted_scores()
        self.assertEqual(formatted_scores, {'imdb_score': 'N/A'})


class RottentomatoesScoresTests(TestCase):
    def setUp(self):
        self.tv_series = TV_Series.objects.create(title="True Detective")
        self.rt_score = RottentomatoesScores.objects.create(
            media=self.tv_series, tomatometer_score=96, audience_score=94)

    def test_tomatometer_score_null_true(self):
        tomatometer_score_null = self.rt_score._meta.get_field(
            "tomatometer_score").null
        self.assertEqual(tomatometer_score_null, True)

    def test_audience_score_null_true(self):
        audience_score_null = self.rt_score._meta.get_field(
            "audience_score").null
        self.assertEqual(audience_score_null, True)

    def test_get_formatted_scores(self):
        formatted_scores = self.rt_score.get_formatted_scores()
        self.assertEqual(formatted_scores, {
                         'tomatometer': '96%', 'audience_score': '94%'})

    def test_get_formatted_scores_returns_na_when_score_values_is_null(self):
        tv_series = TV_Series.objects.create(title="Breaking Bad")
        rt_score = RottentomatoesScores.objects.create(media=tv_series)
        formatted_scores = rt_score.get_formatted_scores()
        self.assertEqual(formatted_scores, {
                         'tomatometer': 'N/A', 'audience_score': 'N/A'})
