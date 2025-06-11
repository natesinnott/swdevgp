#Authored by Nate
from django.urls import path
from .views import ChangePasswordView
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('profile/settings/', ChangePasswordView.as_view(), name="profile-settings"),
]
