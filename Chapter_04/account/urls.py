from django.urls import path
from django.contrib.auth import views as dj_auth_views

from . import views


urlpatterns = [
    # old post view
    # path('login/', views.user_login, name='login'),
    
    path('login/', dj_auth_views.LoginView.as_view(), name='login'),
    path('logout/', dj_auth_views.LogoutView.as_view(), name='logout'),
]