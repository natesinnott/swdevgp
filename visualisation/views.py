#Authored by Eeliya
from django.shortcuts import render
from django.http import JsonResponse
from collections import defaultdict
from .models import Surveyresponsedetail, Surveyresponse, Question, Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import datetime
from django.db.models import F, Func, DateField
from .models import Employee

# render the trends page and show available question categories for filtering
@login_required
def trends(request):
    # get the logged-in employee
    try:
        employee = Employee.objects.filter(user__username=request.user.username).first()
    except Employee.DoesNotExist:
        return render(request, "visualisation/trends.html", {"categories": []})

    # fetch distinct question titles the employee has answered
    question_titles = Question.objects.filter(
        surveyresponsedetail__response__employee=employee
    ).values_list('question_title', flat=True).distinct()

    # render the page with the list of question categories
    return render(request, "visualisation/trends.html", {"categories": question_titles})


# fetch and return data for trends chart as JSON based on filters
@login_required
def trends_data(request):
    # get filter params from request
    selected_type = request.GET.get('type', None)
    selected_category = request.GET.get('category', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # build filters for query based on selected filters
    filters = {}
    if selected_category:
        filters['question__question_title'] = selected_category

    # narrow data based on whether user selected individual/team view
    if selected_type in ['individual', 'team']:
        try:
            employee = Employee.objects.filter(user__username=request.user.username).first()

            if not employee:
                return JsonResponse({"error": "No employee linked to this user."}, status=400)

        except Employee.DoesNotExist:
            return JsonResponse({"error": "No employee linked to this user."}, status=400)

        if selected_type == 'individual':
            filters['response__employee'] = employee
        elif selected_type == 'team':
            filters['response__employee__teamid'] = employee.teamid

    # if date range provided, filter responses within it
    if start_date and end_date:
        try:
            start_date_parsed = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_parsed = datetime.strptime(end_date, "%Y-%m-%d").date()

            all_data = Surveyresponsedetail.objects.select_related("response__session", "question").filter(**filters)
            data = [
                row for row in all_data
                if start_date_parsed <= row.response.session.start_date.date() <= end_date_parsed
            ]
        except Exception as e:
            return JsonResponse({"error": f"Date filtering error: {str(e)}"}, status=400)
    else:
        data = Surveyresponsedetail.objects.select_related("response", "question").filter(**filters)

    # prepare dict to count green, amber, red answers by date
    grouped_data = defaultdict(lambda: {"green": 0, "amber": 0, "red": 0})

    # loop through responses and count answers
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

    # return the structured data as JSON for the frontend chart
    return JsonResponse({
        "dates": dates,
        "green": green,
        "amber": amber,
        "red": red,
    })