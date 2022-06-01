from django.http import JsonResponse
from django.shortcuts import render
from .utils import get_data_from_json
from .forms import SearchForm

# Create your views here.

def homepage(request):
    template = "search.html"
    form = SearchForm()

    context = {'form': form}
    return render(request, template, context)

def scoreboard(request):
    search_term = request.POST.get('search')
    template = "scoreboard.html"

    context = {
        "search_term": search_term,
    }
    return render(request, template, context)

def scoreboard_data(request):
    search_term  = request.GET.get("media")
    mock_data = get_data_from_json("media_ratings/mock-data.json")

    if search_term == "stranger-things":
        mock_data = mock_data["ratingAgencies"][0]
    else:
        mock_data = mock_data["ratingAgencies"][1]
    return JsonResponse(mock_data)