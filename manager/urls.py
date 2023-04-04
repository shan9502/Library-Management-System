from django.urls import path
from .views import (ManageMemberView, DashboardView, 
                    BooksView, AdminLogout, deleteBookView, 
                    SearchBookView, EnableMember, DisableMember,
                    SettingsAdminView, editBookView)


urlpatterns = [
    path('manageMembers/', ManageMemberView),
    path('dashboard/', DashboardView),
    path('books/', BooksView , name= 'books'),
    path('adminlogout/', AdminLogout,name= 'adminlogout'),
    path('deleteBook/', deleteBookView, name="deleteBook"),
    path('searchBook/', SearchBookView, name="searchBook"),
    path(r'^enableMember/(?P<pk>\d+)/$', EnableMember, name="enableMember"),
    path(r'^disableMember/(?P<pk>\d+)/$', DisableMember, name="disableMember"),
    path('settings/', SettingsAdminView, name="settings"),
    path(r'^editBook/(?P<pk>\d+)/$', editBookView, name="editBook"),

]