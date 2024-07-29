from django.contrib import admin
from .models import Message, Notification

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    list_filter = ('timestamp',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'timestamp')
    list_filter = ('notification_type', 'timestamp')

admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)
