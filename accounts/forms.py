from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, Employee, Team

# This form is used to create a new user account. It inherits from UserCreationForm, which provides the basic functionality for creating a user.
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    team = forms.ModelChoiceField(
    queryset=Team.objects.all(),
    empty_label="Select your Team",
    widget=forms.Select(attrs={'placeholder': 'Team'})
)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), help_text=UserCreationForm.base_fields['password1'].help_text)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'team',
        )

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
                    }
       
class ProfileSettingsForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label="Select your Team",
        widget=forms.Select(attrs={'placeholder': 'Team'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        help_text=UserCreationForm.base_fields['password1'].help_text
    )
    new_password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'team')

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        # Only validate passwords if the user is trying to change them
        if new_password1 or new_password2:
            if not current_password:
                self.add_error('current_password', 'Please enter your current password to change your password')
            elif not self.instance.check_password(current_password):
                self.add_error('current_password', 'The current password is incorrect')
            
            if new_password1 != new_password2:
                self.add_error('new_password2', "The two password fields didn't match")
            
            # Validate the new password
            if new_password1:
                from django.contrib.auth.password_validation import validate_password
                try:
                    validate_password(new_password1, self.instance)
                except forms.ValidationError as error:
                    self.add_error('new_password1', error)
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Handle password change if provided
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()
        
        return user
