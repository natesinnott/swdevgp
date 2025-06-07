#Authored by Nate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth import logout



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
def account_view(request):
    return render(request, "accounts/account.html", {"user": request.user})

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "accounts/profile-settings.html"
    def get_success_url(self):
        return '../../../account'

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)