from django.urls import path
from .views import AdminRegView, MemberRegView, AdminLoginView, MemberLoginView

app_name='users'

urlpatterns = [
    path('AdminReg/', AdminRegView),
    path('MemberReg/', MemberRegView),
    path('AdminLogin/', AdminLoginView),
    path(r'^MemberLoginMsg/(?P<msg>\d+)/$', MemberLoginView, name='MemberLoginMsg'),
    path('MemberLogin/', MemberLoginView, name='MemberLogin'),
]
