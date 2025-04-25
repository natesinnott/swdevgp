from django.shortcuts import render, redirect
from django.utils import timezone
from voting.models import Session, SurveyResponse, Employee

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
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

    return render(request, 'dashboard/dashboard.html', {
        'has_active_session': has_active,
        'has_taken': has_taken,
    })

@login_required
def account(request):
    return render(request, "accounts/account.html")