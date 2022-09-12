from django.urls import path
from media_ratings import views

app_name = 'media_ratings'

urlpatterns = [
    path('', views.home, name='home')
]
