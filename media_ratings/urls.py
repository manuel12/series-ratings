from django.urls import path
from media_ratings import views

app_name = 'media_ratings'

urlpatterns = [
    path('', views.homepage, name='home'),
    #path('results/', views.search_result, name='result'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path('fetch-score-data/', views.fetch_score_data, name='fetch-score-data')
]