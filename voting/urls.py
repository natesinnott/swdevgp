from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey, name='voting_survey'),  # main voting page
    path('newsurvey/', views.newsurvey, name='voting_newsurvey'),  # open new survey response page
    path('submit/', views.voting_submit, name='voting_submit'),  # submit survey response
]