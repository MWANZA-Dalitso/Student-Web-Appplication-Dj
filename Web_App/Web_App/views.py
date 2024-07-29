from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')

def testimonials(request):
    return render(request, 'testimonials.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def settings(request):
    return render(request, 'settings.html')
