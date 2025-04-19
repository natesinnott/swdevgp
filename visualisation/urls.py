from django.urls import path
from . import views

urlpatterns = [
    path("", views.trends, name="visualisation"),
    path("data/", views.trends_data, name="trends-data"), # TODO: front-end should use this URL to fetch data for the chart
]