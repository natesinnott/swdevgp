from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def trends(request):
    return render(request, "visualisation/trends.html")

@login_required
def trends_data(request):
    """
    TODO: Replace the dummy data below with real QuerySets against models.
    - Filter by request.user (if individual) or by team
    - Filter by selected category/start/end quarter (from request.GET)
    - Aggregate counts into lists for each sentiment
    """
    # Example of expected JSON shape:
    data = {
        "quarters": ["Q2 24", "Q3 24", "Q4 24"],
        "great":    [5, 15, 30],
        "decent":   [10, 24, 25],
        "terrible": [25, 20,  2],
    }
    return JsonResponse(data)