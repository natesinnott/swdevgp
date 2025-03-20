from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, Employee, Team

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'team'
        )