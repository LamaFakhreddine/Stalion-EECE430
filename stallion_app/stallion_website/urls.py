from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('about/', views.about, name="about"),
    path('contactUs/', views.contact, name="contactUs"),
    path('programs/', views.programs, name='programs'),
    path('programinfo/', views.programinfo, name='programinfo'),
    path('reserve/', views.reserve, name='reserve'),
    path('reserveinfo/', views.reserveinfo, name='reserveinfo'),
    path('buytickets/', views.buytickets, name="buytickets"),
    path('enroll/', views.enroll, name="enroll"),

    path('login/', views.loginPage, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logoutUser, name="logout"),

	path('login/memberAccount/', views.member, name="memberAccount"),
    path('login/coachAccount/', views.coach, name="coachAccount"),
    path('adminAccount/', views.admin, name="adminAccount"),
    path('#', views.profile, name="profile"),
    path('members/', views.members, name="members"),

    path('delete_member/<str:m>', views.delete_member, name='delete_member'),
    path('filter_member/', views.filter_member, name='filter_member'),
    path('update_member/<str:m>', views.update_member, name='update_member'),
    path('save_updates/', views.save_updates, name='save_updates')

    
]
