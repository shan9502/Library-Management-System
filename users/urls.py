from django.urls import path
from .views import AdminRegView, MemberRegView, AdminLoginView, MemberLoginView

urlpatterns = [
    path('AdminReg/', AdminRegView),
    path('MemberReg/', MemberRegView),
    path('AdminLogin/', AdminLoginView),
    path('MemberLogin/', MemberLoginView),
]
