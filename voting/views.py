from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils        import timezone
from .models             import Session, Survey, SurveyResponse, Employee

# Create your views here.

@login_required
def survey(request):
    # find an open session by datetime
    now = timezone.now()
    sessions_qs = Session.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    )
    has_active = sessions_qs.exists()
    active_session = sessions_qs.first()
    has_taken = False
    if active_session:
        has_taken = SurveyResponse.objects.filter(
            employee__user=request.user,
            session=active_session
        ).exists()

    print(f"[Survey View] now = {now}")
    print(f"[Survey View] sessions_qs = {list(sessions_qs)}")
    print(f"[Survey View] has_active = {has_active}")
    print(f"[Survey View] active_session = {active_session}")
    print(f"[Survey View] has_taken = {has_taken}")

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
    active = Session.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    ).first()

    print(f"[NewSurvey View] now = {now}")
    print(f"[NewSurvey View] active = {active}")

    # Prevent repeat submissions
    if SurveyResponse.objects.filter(employee__user=request.user, session=active).exists():
        return redirect('voting_survey')

    # 2) If none, bounce back with a message
    if not active:
        return redirect('voting_survey')

    # 3) Otherwise proceed to newsurvey.html
    questions = Survey.objects.get(pk=active.survey_id)
    return render(request, 'voting/newsurvey.html', {
        'session':   active,
        'questions': questions,
    })