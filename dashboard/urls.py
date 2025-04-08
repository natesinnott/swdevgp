from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="dashboard"),  # Home/Dashboard page
    path('account/', views.account, name='account'),  # Account page
]