from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('register/', views.register, name="register"),
	path('login/memberAccount/', views.member, name="memberAccount"),
    path('login/coachAccount/', views.coach, name="coachAccount")
]
