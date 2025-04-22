from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey, name='voting_survey'),  # main voting page
    path('newsurvey/', views.newsurvey, name='voting_newsurvey'),  # another example page
]