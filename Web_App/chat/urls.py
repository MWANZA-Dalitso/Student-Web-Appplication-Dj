from django.urls import path
from . import views

from .views import chat_view, start_chat  # Add this line

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('notifications/', views.notifications, name="notifications"),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('chat_view/', chat_view, name='chat_view'),  # Update this line
    path('start_chat/', start_chat, name='start_chat'),  # Update this line
]
