from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('users/', include('teams.users.urls') ),
    path('teams/',include('teams.teamsapp.urls'))
]
