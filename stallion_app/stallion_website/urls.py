from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('about/', views.about, name="about"),
    path('contactUs/', views.contact, name="contactUs"),

    path('login/', views.loginPage, name="login"),
    path('signup/', views.signup, name="signup"),
     path('logout/', views.logoutUser, name="logout"),

	path('login/memberAccount/', views.member, name="memberAccount"),
    path('login/coachAccount/', views.coach, name="coachAccount"),
    path('adminAccount/', views.admin, name="adminAccount"),
    path('#', views.profile, name="profile")

    
]
