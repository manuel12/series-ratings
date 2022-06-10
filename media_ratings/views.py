from turtle import title
from django.http import JsonResponse
from django.shortcuts import render
from .forms import SearchForm
from .utils import load_json_data, capitalize_phrase, sanitize_phrase, standardize_phrase
from .parsers import IMDbMediaPageParser, RottentomatoesMediaPageParser
from .search_parser import IMDBSearchResultsParser, RottentomatoesSearchResultsParser
from .models import *

# Create your views here.


def homepage(request):
    template = "search.html"
    form = SearchForm()

    context = {'form': form}
    return render(request, template, context)


def scoreboard(request):
    search_term = request.POST.get('search')
    template = "scoreboard.html"

    capitalized_search_term = capitalize_phrase(search_term)
    sanitized_search_term = sanitize_phrase(search_term)
    context = {
        "media_title": capitalized_search_term,
        "search_term": sanitized_search_term

    }
    # context.update(rating_values)
    return render(request, template, context)


def fetch_score_data(request):
    imdb_score_value = 0
    rt_tomatometer_value = 0
    rt_audience_score_value = 0

    search_term = request.GET.get("media")
    search_term = standardize_phrase(search_term)
    print(search_term)

    tv_series = TV_Series.objects.filter(title=search_term).first()

    if(tv_series):
        print(f"Series found: {tv_series}")
        print("Checking if records are present...")
        imdb_score = tv_series.imdb_scores()["imdb_score"]
        rt_tomatometer = tv_series.rottentomatoes_scores()["tomatometer"]
        rt_audience_score = tv_series.rottentomatoes_scores()["audience_score"]

        if "N/A" in (imdb_score, rt_tomatometer, rt_audience_score):
            print("N/A found on one or more records. Fetching data from the web...")
            # Call function to ONLY fetch score data for the current 'tv_series'.
            # Might need to pass the tv_series title on to the search parsers in order
            # to get the score page urls.
        else:
            scores_data = {
                "imdb": imdb_score,
                "rt": {
                    "tomatometer": rt_tomatometer,
                    "audience-score": rt_audience_score
                }
            }

        return JsonResponse(scores_data)

    else:
        print("Series not found!")
        print("Fetching data from the web...")
        # try:
        print(
            f"-----------------------------------------{search_term}----------------------------------------------------")
        imdb_score, rt_tomatometer, rt_audience_score = search_parse_and_save_score_data(
            search_term, imdb_score_value, rt_tomatometer_value, rt_audience_score_value)

        scores_data = {
            "imdb": imdb_score,
            "rt": {
                "tomatometer": rt_tomatometer,
                "audience-score": rt_audience_score
            }
        }
        return JsonResponse(scores_data)


def search_parse_and_save_score_data(search_term, imdb_score_value, rt_tomatometer_value, rt_audience_score_value):
    urls = get_search_result_urls(search_term)
    imdb_parser = IMDbMediaPageParser(urls["imdb"])
    rt_parser = RottentomatoesMediaPageParser(urls["rottentomatoes"])

    imdb_score_value, rt_tomatometer_value, rt_audience_score_value = fetch_scores(imdb_parser, rt_parser, imdb_score_value,
                                                                                   rt_tomatometer_value, rt_audience_score_value)

    print_statements(
        imdb_score_value,
        rt_tomatometer_value,
        rt_audience_score_value)
    print("Saving values in the database...")

    new_series = create_new_series(search_term)
    create_new_imdb_score(new_series, imdb_score_value)
    create_new_rt_score(
        new_series, rt_tomatometer_value, rt_audience_score_value)
    
    imdb_score = new_series.imdb_scores()["imdb_score"]
    rt_tomatometer = new_series.imdb_scores()["imdb_score"]
    rt_audience_score = new_series.imdb_scores()["imdb_score"]
    
    return [imdb_score, rt_tomatometer, rt_audience_score]


def get_search_result_urls(search_term):
    imdb_search_parser = IMDBSearchResultsParser(search_term)
    rtSearchParser = RottentomatoesSearchResultsParser(search_term)
    return {
        "imdb": imdb_search_parser.get_search_result_url(),
        "rottentomatoes": rtSearchParser.get_search_result_url()
    }


def fetch_scores(imdb_page_parser, rt_page_parser, imdb_score_value, rt_tomatometer_value, rt_audience_score_value):
    imdb_score_value = imdb_page_parser.get_score_value()
    print("Fetched imdb score data...")

    rt_tomatometer_value = rt_page_parser.get_tomatometer_value()
    print("Fetched rt tomatometer data...")

    rt_audience_score_value = rt_page_parser.get_audience_score_value(
    )
    print("Fetched rt audience_score data...")
    return [imdb_score_value, rt_tomatometer_value, rt_audience_score_value]


def create_new_series(title):
    new_series = TV_Series.objects.create(title=title)
    print("Created new series...")
    new_series.save()
    print("Saved new series...")
    return new_series


def create_new_imdb_score(series, score):
    new_imdb_score = IMDbScores.objects.create(
        media=series,
        imdb_score=score)
    print("Created new IMDb score...")

    new_imdb_score.save()
    print("Saved new IMDb score...")
    return new_imdb_score


def create_new_rt_score(series, tomatometer_score, audience_score):
    rt_tomatometer_score = tomatometer_score
    rt_audience_score = audience_score

    new_rt_score = RottentomatoesScores.objects.create(
        media=series,
        tomatometer_score=rt_tomatometer_score,
        audience_score=rt_audience_score)
    print("Created new RT score...")

    new_rt_score.save()
    print("Saved new RT score...")


def print_statements(st1, st2, st3):
    print(f'---- imdb score: {st1}')
    print(f'---- rottentomatoes tomatometer: {st2}')
    print(f'---- rottentomatoes audience: {st3}')
