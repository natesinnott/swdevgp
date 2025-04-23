from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils        import timezone
from .models             import Session, SurveyResponse, SurveyDetail, SurveyResponseDetail, Employee

# Create your views here.

@login_required
def survey(request):
    # find an open session by datetime
    now = timezone.now()
    # Get the Employee record for the logged-in user
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('dashboard')

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

    return render(request, 'voting/survey.html', {
        'has_active_session': has_active,
        'has_taken': has_taken
    })

@login_required
def newsurvey(request):
    if request.method != 'POST':
        return redirect('voting_survey')

    # find open session by datetime
    now = timezone.now()
    # Get the Employee record for the logged-in user
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('voting_survey')

    active = Session.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    ).first()

    # Prevent repeat submissions
    if SurveyResponse.objects.filter(employee=employee, session=active).exists():
        return redirect('voting_survey')

    # 2) If none, bounce back with a message
    if not active:
        return redirect('voting_survey')

    # 3) Otherwise proceed to newsurvey.html
    questions = active.survey.questions.all()
    return render(request, 'voting/newsurvey.html', {
        'session':   active,
        'questions': questions,
    })


# voting_submit view to handle survey submission
from django.contrib import messages

@login_required
def voting_submit(request):
    if request.method != 'POST':
        return redirect('voting_survey')
    
    # Debug: print submitted form data
    print("voting_submit POST data:", dict(request.POST))


    # find the active session
    now = timezone.now()
    active = Session.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    ).first()
    if not active:
        messages.error(request, "No active survey session found.")
        return redirect('voting_survey')

    # get the employee record
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "Employee profile not found.")
        return redirect('voting_survey')

    # prevent duplicate submissions
    if SurveyResponse.objects.filter(employee=employee, session=active).exists():
        messages.info(request, "You have already submitted this Health Check.")
        return redirect('voting_survey')

    # create a new SurveyResponse
    response = SurveyResponse.objects.create(
        employee=employee,
        survey=active.survey,
        session=active
    )

    # iterate through each question in this survey
    details = SurveyDetail.objects.filter(survey=active.survey)
    for detail in details:
        qid = detail.question.id
        # extract answers from POST data
        answer = request.POST.get(f'health-{qid}')
        trend  = request.POST.get(f'trend-{qid}')
        comment = request.POST.get(f'comments-{qid}', '').strip()
        # create a detail record
        SurveyResponseDetail.objects.create(
            response=response,
            question=detail.question,
            answer=answer,
            improvement_state=trend,
            comment=comment
        )

    messages.success(request, "Thank you for completing the Health Check!")
    return render(request, 'voting/survey_complete.html')