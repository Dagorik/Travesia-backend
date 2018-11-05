from django.contrib import admin
from django.urls import path
from teams.users import views
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('me/', views.MeView.as_view()),


]