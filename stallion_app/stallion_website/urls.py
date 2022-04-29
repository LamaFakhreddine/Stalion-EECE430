from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('about/', views.about, name="about"),
    path('contactUs/', views.contact, name="contactUs"),
    path('programs/', views.programs, name="programs"),
    path('programinfo/', views.programinfo, name="programinfo"),
    path('reserve/', views.reserve, name="reserve"),
    path('reserveinfo/', views.reserveinfo, name="reserveinfo"),
    path('buytickets/', views.buytickets, name="buytickets"),
    path('enroll/', views.enroll, name="enroll"),
    path('reservation/', views.reservation, name="reservation"),

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
    path('save_updates/', views.save_updates, name='save_updates'),

    path('coaches/', views.coaches, name="coaches"),
    path('delete_coaches/<str:m>', views.delete_coaches, name='delete_coaches'),
    path('filter_coaches/', views.filter_coaches, name='filter_coaches'),
    path('update_coaches/<str:m>', views.update_coaches, name='update_coaches'),
    path('save_updates2/', views.save_updates2, name='save_updates2'),
    path('add_coaches/', views.add_coaches, name='add_coaches'),

    path('programs_admin/', views.programs_admin, name='programs_admin'),
    path('delete_programs/<str:m>', views.delete_programs, name='delete_programs'),
    path('filter_programs/', views.filter_programs, name='filter_programs'),
    path('update_programs/<str:m>', views.update_programs, name='update_programs'),
    path('save_updates3/', views.save_updates3, name='save_updates3'),
    path('add_programs/', views.add_programs, name='add_programs'),

    path('courts/', views.courts, name='courts'),
    path('delete_courts/<str:m>', views.delete_courts, name='delete_courts'),
    path('filter_courts/', views.filter_courts, name='filter_courts'),
    path('update_courts/<str:m>', views.update_courts, name='update_courts'),
    path('save_updates4/', views.save_updates4, name='save_updates4'),
    path('add_courts/', views.add_courts, name='add_courts'),

    path('events_admin/', views.events_admin, name='events_admin'),
    path('delete_events/<str:m>', views.delete_events, name='delete_events'),
    path('filter_events/', views.filter_events, name='filter_events'),
    path('update_events/<str:m>', views.update_events, name='update_events'),
    path('save_updates5/', views.save_updates5, name='save_updates5'),
    path('add_events/', views.add_events, name='add_events')

    

    
]
