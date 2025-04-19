from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def trends(request):
    return render(request, "visualisation/trends.html")