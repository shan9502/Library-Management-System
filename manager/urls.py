from django.urls import path
from .views import (ManageMemberView, DashboardView, 
                    BooksView, AdminLogout, deleteBookView, 
                    SearchBookView, EnableMember, DisableMember,
                    SettingsAdminView, editBookView, TransactionsView, ProfileView)

app_name='manager'

urlpatterns = [
    path('manageMembers/', ManageMemberView),
    path('dashboard/', DashboardView,name='dashboard'),
    path('books/', BooksView , name= 'books'),
    path('adminlogout/', AdminLogout,name= 'adminlogout'),
    path('deleteBook/', deleteBookView, name="deleteBook"),
    path('searchBook/', SearchBookView, name="searchBook"),
    path(r'^enableMember/(?P<pk>\d+)/$', EnableMember, name="enableMember"),
    path(r'^disableMember/(?P<pk>\d+)/$', DisableMember, name="disableMember"),
    path('settings/', SettingsAdminView, name="settings"),
    path('editBook/', editBookView, name="editBook"),
    #path(r'^manageReservations/(?P<pk>\d+)/$', ManageReservationsView, name="manageReservations"),
    path('transactions/', TransactionsView,name='transactions'),
    path('profile/', ProfileView,name='profile'),
]