from django.urls import path
from .views import register, login_view, logout_view, profile, settings, profile_dashboard, CustomPasswordChangeView

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/dashboard/', profile_dashboard, name='profile_dashboard'),
    path('settings/', settings, name='settings'),
    path('settings/password/', CustomPasswordChangeView.as_view(), name='password_change'),
]
