from django.db import models

# Create your models here.


class Media(models.Model):
    """
    Base class for representing a media instance.

    Should not be used directly but extended instead.
    """

    title = models.CharField(
        max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Medias"

    def __str__(self):
        return self.title

    def imdb_scores(self):
        imdb_score_instance = IMDbScores.objects.filter(media=self).first()

        if not imdb_score_instance:
            imdb_score_instance = IMDbScores.objects.create(
                media=self, imdb_score=None)

        return imdb_score_instance.imdb_score

    def rottentomatoes_scores(self):
        rt_score_instance = RottentomatoesScores.objects.filter(
            media=self).first()

        if not rt_score_instance:
            rt_score_instance = RottentomatoesScores.objects.create(
                media=self, tomatometer_score=None, audience_score=None)

        return rt_score_instance.tomatometer_score, rt_score_instance.audience_score


class TV_Series(Media):
    num_seasons = models.IntegerField(blank=True, default=1)
    num_eps_per_season = models.IntegerField(blank=True, default=1)
    num_eps = models.IntegerField(blank=True, default=1)

    class Meta:
        verbose_name_plural = "TV Series"


class MediaScore(models.Model):
    """
    Base class for representing a media scores.

    Should not be used directly but extended instead.
    """

    media = models.ForeignKey(TV_Series, on_delete=models.CASCADE)

    def __str__(self):
        return f"{TV_Series} scores"

    class Meta:
        verbose_name_plural = "TV_Series Scores"


class IMDbScores(MediaScore):
    imdb_score = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "IMDb Scores"

    def __str__(self):
        return f"IMDbScore of ({self.imdb_score}/10) for media {self.media}"


class RottentomatoesScores(MediaScore):
    tomatometer_score = models.IntegerField(null=True)
    audience_score = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Rottentomatoes Scores"

    def __str__(self):
        return f"RottentomatoesScore of tomatometer ({self.tomatometer_score}%) and audience score ({self.audience_score}%) for media {self.media}"
