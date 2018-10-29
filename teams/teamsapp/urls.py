from django.contrib import admin
from django.urls import path
from teams.teamsapp import views


urlpatterns = [
    path('/', views.CreateTeams.as_view()),

]