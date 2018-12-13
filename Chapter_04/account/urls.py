from django.urls import path, include
from django.contrib.auth import views as dj_auth_views

from . import views


urlpatterns = [
    # old post view
    # path('login/', views.user_login, name='login'),
    
    # [WARNING] REPLACED BY 'django.contrib.auth.urls'
    # path('login/', dj_auth_views.LoginView.as_view(), name='login'),
    # path('logout/', dj_auth_views.LogoutView.as_view(), name='logout'),
    
    # [WARNING] REPLACED BY 'django.contrib.auth.urls'
    # path('password_change/',
    #      dj_auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/',
    #      dj_auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # path('password_reset/',
    #      dj_auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/',
    #      dj_auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    # [WARNING] REPLACED BY 'django.contrib.auth.urls'
    # path('reset/<uidb64>/<token>/',
    #      dj_auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/',
    #      dj_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # This one line could take over
    #   all the jobs we've done in the ↑ six lines above :P
    path('', include('django.contrib.auth.urls')),
    
    # we actually only need these two lines
    #   1. auth part (done by Django, of course we can customize it)
    #   2. our part  (that's up to you, right? XD)
    path('', views.dashboard, name='dashboard'),
]