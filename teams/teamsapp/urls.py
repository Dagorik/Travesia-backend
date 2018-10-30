from django.contrib import admin
from django.urls import path
from teams.teamsapp import views


urlpatterns = [
    path('create/', views.CreateTeam.as_view()),

]