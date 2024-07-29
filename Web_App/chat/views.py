from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib.auth.models import User
from django.urls import reverse

@login_required
def chat(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'chat/chat.html', {'notifications': notifications})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'chat/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def chat_view(request):
    users = User.objects.exclude(username=request.user.username)  # Exclude current user from the list
    return render(request, 'chat/chat.html', {'users': users})

@login_required
def start_chat(request):
    if request.method == 'POST':
        selected_user = request.POST.get('selected_user')
        if selected_user:
            return redirect(reverse('chat_view') + f'?user={selected_user}')
    return redirect('chat_view')  # Redirect back to chat view if no user selected
