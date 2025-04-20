from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def survey(request):
    return render(request, 'voting/survey.html')

@login_required
def newsurvey(request):
    return render(request, 'voting/newsurvey.html')