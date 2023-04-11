from django.urls import path
from .views import ( HomeView, MemberLogoutView ,ReservationsView, BookIssuesView)

app_name='member'

urlpatterns = [
    path('home/', HomeView, name='home'),
    path('memberLogout/', MemberLogoutView, name='memberLogout'),
    path('reservations/', ReservationsView, name='reservations'),
    path('issued/', BookIssuesView, name='issued'),


]