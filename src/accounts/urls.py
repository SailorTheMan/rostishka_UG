from django.conf.urls import url
from . import views
from django.urls import path, include
from accounts.views import signup, activate, two_factor_login, profile_view

urlpatterns = [
    # post views
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    path('<uidb64>/<token>/', activate, name='activate'),
    path('login/<uidb64>/<token>/', two_factor_login, name='two_factor_login'),
    path('profile', profile_view, name='profile'),
]