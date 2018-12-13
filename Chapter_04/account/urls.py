from django.urls import path
from django.contrib.auth import views as dj_auth_views

from . import views


urlpatterns = [
    # old post view
    # path('login/', views.user_login, name='login'),
    
    path('login/', dj_auth_views.LoginView.as_view(), name='login'),
    path('logout/', dj_auth_views.LogoutView.as_view(), name='logout'),
    
    path('', views.dashboard, name='dashboard'),
    
    path('password_change/',
         dj_auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',
         dj_auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('password_reset/',
         dj_auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/',
         dj_auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         dj_auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',
         dj_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]