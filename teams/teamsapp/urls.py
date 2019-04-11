from django.contrib import admin
from django.urls import path
from teams.teamsapp import views


urlpatterns = [
    path('create/', views.CreateTeam.as_view()),
    path('join/', views.JoinTeam.as_view()),
    path('', views.RetrieveTeams.as_view()),
    path('<uuid:id>/', views.GetTeam.as_view()),
    path('remove/', views.LeaveTeam.as_view()),
    path('checkpoint/', views.ListCheckpoints.as_view()),
	path('checkpoint/<uuid:id>/', views.GetCheckPoint.as_view()),
	path('track/', views.AddTrack.as_view()),
	path('position/', views.CheckPosition.as_view()),
	path('leaderboard/', views.LeaderBoardList.as_view()),






]
