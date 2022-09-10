from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from media_ratings.score_fetcher import ScoreFetcher

# Create your views here.


@api_view(('GET',))
def fetch_score_data(request):
    search_term = request.GET.get("media")

    if search_term:
        score_fetcher = ScoreFetcher(search_term)
        standardized_search_term = score_fetcher.get_starndardized_search_term()
        print(f"-- SEARCH TERM: {standardized_search_term}")
        score_data = score_fetcher.get_score_data()
        print(score_data)
        return JsonResponse(score_data, status=200, safe=False)
    return Response({}, status=200)
