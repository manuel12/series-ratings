from rest_framework import serializers
from media_ratings import models


class TV_SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TV_Series
        fields = ("title", "imdb_scores", "rottentomatoes_scores")


class IMDbScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IMDbScores
        fields = ("media", "imdb_score")


class RotttenTomatoesScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RottentomatoesScores
        fields = ("media", "tomatometer_score", "audience_score")
