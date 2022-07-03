from django.db import models

# Create your models here.

class Media(models.Model):
    """
    Base class for representing a media instance.

    Should not be used directly but extended instead.
    """

    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True)

    def imdb_scores(self):
        imdb_score = None
        imdb_score_instance = IMDbScores.objects.filter(media=self).first()
        
        if imdb_score_instance:
              imdb_score = imdb_score_instance.imdb_score
        return {
            "imdb_score": f"{imdb_score}/10" if imdb_score else "N/A"
        }

    class Meta:
        verbose_name_plural = "Medias"

    def rottentomatoes_scores(self):
        tomatometer_score = None
        audience_score = None
        rt_score_instance = RottentomatoesScores.objects.filter(media=self).first()

        if rt_score_instance:
            tomatometer_score = rt_score_instance.tomatometer_score
            audience_score = rt_score_instance.audience_score
        return {
          "tomatometer": f"{tomatometer_score}%" if tomatometer_score else 'N/A',
          "audience_score": f"{audience_score}%" if audience_score else 'N/A'
        }

    def __str__(self):
        return self.title


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

    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return f"{Media} scores"

    class Meta:
        verbose_name_plural = "Media Scores"


class IMDbScores(MediaScore):
    imdb_score = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "IMDb Scores"

    def get_formatted_scores(self):
        return {
            "imdb_score": f"{self.imdb_score}/10" if self.imdb_score else "N/A"
        }


class RottentomatoesScores(MediaScore):
    tomatometer_score = models.IntegerField(null=True)
    audience_score = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Rottentomatoes Scores"

    def get_formatted_scores(self):
        return {
          "tomatometer": f"{self.tomatometer_score}%" if self.tomatometer_score else 'N/A',
          "audience_score": f"{self.audience_score}%" if self.audience_score else 'N/A'
        }