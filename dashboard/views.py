from django.shortcuts import render, redirect
from django.utils import timezone
from collections import defaultdict
from django.http import JsonResponse
from voting.models import Session, SurveyResponse, Employee, SurveyResponseDetail

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
        # find an open session by datetime
    now = timezone.now()
    # Get the Employee record for the logged-in user
    try:
        employee = Employee.objects.get(user=request.user)
        jobTitle = employee.jobTitle
    except Employee.DoesNotExist:
        return render(request, 'dashboard/unverified.html', {
            'message': 'Your account needs to be verified by a Sky UK admin before access is granted to this application.'
        })

    sessions_qs = Session.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    )
    has_active = sessions_qs.exists()
    active_session = sessions_qs.first()
    has_taken = False
    if active_session:
        has_taken = SurveyResponse.objects.filter(
            employee=employee,
            session=active_session
        ).exists()

    return render(request, 'dashboard/dashboard.html', {
        'has_active_session': has_active,
        'has_taken': has_taken,
        'jobTitle': jobTitle,
    })

@login_required
def account(request):
    return render(request, "accounts/account.html")


# Trends data for the latest session, grouped for all questions, bar graph
from django.views.decorators.http import require_GET

@login_required
@require_GET
def trends_data(request):
    try:
        latest_session = Session.objects.latest("start_date")
    except Session.DoesNotExist:
        return JsonResponse({"error": "No sessions available."}, status=400)

    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee record not found."}, status=404)

    data = SurveyResponseDetail.objects.select_related("response__session", "question").filter(
        response__session=latest_session,
        response__employee=employee
    )

    grouped_data = defaultdict(lambda: {"green": 0, "amber": 0, "red": 0})

    for row in data:
        start_date = row.response.session.start_date.date()
        date_str = start_date.strftime("%Y-%m-%d")
        answer = row.answer.lower()
        if answer in grouped_data[date_str]:
            grouped_data[date_str][answer] += 1

    dates = sorted(grouped_data.keys())
    green = [grouped_data[d]["green"] for d in dates]
    amber = [grouped_data[d]["amber"] for d in dates]
    red = [grouped_data[d]["red"] for d in dates]

    return JsonResponse({
        "dates": dates,
        "green": green,
        "amber": amber,
        "red": red,
    })
