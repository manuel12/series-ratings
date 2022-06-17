from django.test import TestCase
from .models import TV_Series, IMDbScores, RottentomatoesScores
from .score_manager import ScoreManager

# Create your tests here.

class ScoreManagerTests(TestCase):
    def setUp(self):
        search_term = "True Detective"
        
        self.tv_series = TV_Series.objects.create(title="True Detective")
        score_manager = ScoreManager(search_term)
        self.score_data = score_manager.get_score_data()
        
    def test_all_score_values(self):
        print(self.score_data)
        self.assertEqual(self.score_data["imdb"], 8.9)
        self.assertEqual(self.score_data["rt"]["tomatometer"], 78)
        self.assertEqual(self.score_data["rt"]["audience_score"], 75)
        

class ScoreManagerIMDbScoreTests(TestCase):
    def setUp(self):
        search_term = "True Detective"
        
        self.tv_series = TV_Series.objects.create(title="True Detective")
        rt_scores = RottentomatoesScores.objects.create(
            media=self.tv_series, tomatometer_score=98, audience_score=99)
        
        score_manager = ScoreManager(search_term)
        self.score_data = score_manager.get_score_data()
        
    def test_imdb_score_values(self):
        print(self.score_data)
        self.assertEqual(self.score_data["imdb"], 8.9)
    

class ScoreManagerRottentomatoesScoreTests(TestCase):
    def setUp(self):
        search_term = "True Detective"
        
        self.tv_series = TV_Series.objects.create(title="True Detective")
        imdb_score = IMDbScores.objects.create(
            media=self.tv_series, imdb_score=10)
        
        score_manager = ScoreManager(search_term)
        self.score_data = score_manager.get_score_data()
        
    def test_imdb_score_values(self):
        print(self.score_data)
        self.assertEqual(self.score_data["rt"]["tomatometer"], 78)
        self.assertEqual(self.score_data["rt"]["audience_score"], 75)
    
    
class ScoreManagerNoDataAvailableTests(TestCase):
    def setUp(self):
        search_term = "True Detective"        
        self.score_manager = ScoreManager(search_term)
        self.score_data = self.score_manager.get_score_data()

    def test_series_and_all_score_values(self):
        print(self.score_data)
        
        self.assertEqual(str(self.score_manager.tv_series), "True Detective")
        self.assertEqual(self.score_data["imdb"], 8.9)
        self.assertEqual(self.score_data["rt"]["tomatometer"], 78)
        self.assertEqual(self.score_data["rt"]["audience_score"], 75)