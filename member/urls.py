from django.urls import path
from .views import ( HomeView, MemberLogoutView )
app_name='member'
urlpatterns = [
    path('home/', HomeView, name='home'),
    path('memberLogout/', MemberLogoutView, name='memberLogout'),
]