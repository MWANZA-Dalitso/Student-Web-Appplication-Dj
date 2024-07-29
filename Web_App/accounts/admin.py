from django.contrib import admin
from .models import Profile, University, LevelOfStudy

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_name', 'email', 'university', 'level_of_study']
    list_filter = ['university', 'level_of_study']
    search_fields = ['user__username', 'student_name', 'email']

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(LevelOfStudy)
class LevelOfStudyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


