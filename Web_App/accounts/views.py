from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserRegisterForm, ProfileUpdateForm, ProfileEditForm, ProfileForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Check if a profile already exists for the user
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)
            
            messages.success(request, 'Registration successful. You are now logged in.')
            login(request, user)  # Log the user in immediately after registration
            return redirect('dashboard')  # Redirect to the dashboard or home page
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {'p_form': p_form})

@login_required
def profile_dashboard(request):
    profile_data = Profile.objects.filter(user=request.user).first()
    return render(request, 'registration/profile_dashboard.html', {'profile_data': profile_data})

@login_required
def settings(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'settings.html', {'form': form})

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password-change.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('settings')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')



def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            # Additional validation or processing logic
            profile.save()
            return redirect('profile_created_successfully')
    else:
        form = ProfileForm()
    
    return render(request, 'create_profile.html', {'form': form})
