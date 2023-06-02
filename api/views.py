from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from media_ratings.score_fetcher import get_score_data

# Create your views here.


@api_view(('GET',))
def fetch_score_data(request):
    search_term = request.GET.get("media")

    if search_term:
        score_data, search_term = get_score_data(search_term)
        print(f"-- {score_data}, {search_term}")
        return JsonResponse(
            {"data": score_data, "title": search_term},
            status=200, safe=False)
    return Response({}, status=200)
