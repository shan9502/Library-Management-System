from django.urls import path
from .views import ManageMemberView, DashboardView, BooksView, AdminLogout, AddBook

urlpatterns = [
    path('ManageMembers', ManageMemberView),
    path('dashboard', DashboardView),
    path('books', BooksView),
    path('addbooks', AddBook),
    path('adminlogout', AdminLogout),
]