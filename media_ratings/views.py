from django.http import JsonResponse
from django.shortcuts import render
from .forms import SearchForm
from .utils import capitalize_phrase, sanitize_phrase
from .score_manager import ScoreManager

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
    return render(request, template, context)


def fetch_score_data(request):
    search_term = request.GET.get("media")
    
    sc = ScoreManager(search_term)
    score_data = sc.get_score_data()
    return JsonResponse(score_data)
