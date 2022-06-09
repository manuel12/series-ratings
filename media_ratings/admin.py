from pydoc import describe
from django.contrib import admin
from media_ratings.models import *

# Register your models here.

class MediaAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    
class TV_SeriesAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "num_seasons", "num_eps_per_season", "num_eps"]
    
class MediaScoreAdmin(admin.ModelAdmin):
    list_display = ["media"]
    
class IMDbScoresAdmin(admin.ModelAdmin):
    list_display = ["media", "imdb_score"]
    
class RottentomatoesScoresAdmin(admin.ModelAdmin):
    list_display = ["media", "tomatometer_score", "audience_score"]
    

admin.site.register(Media, MediaAdmin)
admin.site.register(TV_Series, TV_SeriesAdmin)
admin.site.register(MediaScore, MediaScoreAdmin)
admin.site.register(IMDbScores, IMDbScoresAdmin)
admin.site.register(RottentomatoesScores, RottentomatoesScoresAdmin)