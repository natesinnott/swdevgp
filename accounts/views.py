#Authored by Nate
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileSettingsForm
from .models import Employee
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
      
            login(request, user)
            return redirect("dashboard")
        
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # If password was changed, update the session to keep the user logged in
            if form.cleaned_data.get('new_password1'):
                update_session_auth_hash(request, user)
                messages.success(request, 'Your profile and password have been updated successfully.')
            else:
                messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile-settings')
    else:
        form = ProfileSettingsForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'accounts/profile-settings.html', context)

# Create your views here.
