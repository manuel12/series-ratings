from django.urls import path
from .views import fetch_score_data

urlpatterns = [
  path("", fetch_score_data)
]