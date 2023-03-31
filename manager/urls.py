from django.urls import path
from .views import ManageMemberView, DashboardView, BooksView, AdminLogout, deleteBookView


urlpatterns = [
    path('ManageMembers/', ManageMemberView),
    path('dashboard/', DashboardView),
    path('books/', BooksView , name= 'books'),
    path('adminlogout/', AdminLogout,name= 'adminlogout'),
    path('deleteBook/', deleteBookView, name="deleteBook"),
]