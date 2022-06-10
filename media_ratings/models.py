from django.db import models

# Create your models here.

class Media(models.Model):
    """Base class for representing a media instance.
    Should not be used directly and extended instead."""
    
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True)
    
    def imdb_scores(self):
        imdb_score_instance = IMDbScores.objects.filter(media=self).first()
        
        if(imdb_score_instance):
            print(f"-- IMDb score instance found for media: {self}")
            return {
                "imdb_score": f"{imdb_score_instance.imdb_score}/10"
            }
        else:
            return {
                "imdb_score":   "N/A"
            }

    class Meta:
        verbose_name_plural = "Medias"

    def rottentomatoes_scores(self):
        rt_score_instance = RottentomatoesScores.objects.filter(media=self).first()
        
        if(rt_score_instance):
            print(f"-- RT score instance found for media: {self}")
            return {
                "tomatometer": f"{rt_score_instance.tomatometer_score}%",
                "audience_score": f"{rt_score_instance.audience_score}%"
            }
        else:
            return {
                "tomatometer": "N/A",
                "audience_score": "N/A"
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
    """Base class for representing a media scores.
    Should not be used directly and extended instead."""
    
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{Media} scores"

    class Meta:
        verbose_name_plural = "Media Scores"
    
class IMDbScores(MediaScore):
    imdb_score = models.FloatField(blank=True)

    class Meta:
        verbose_name_plural = "IMDb Scores"

class RottentomatoesScores(MediaScore):
    tomatometer_score = models.IntegerField(blank=True)
    audience_score = models.IntegerField(blank=True)

    class Meta:
        verbose_name_plural = "Rottentomatoes Scores"