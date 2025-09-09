from django.contrib import admin

# Register your models here.
from .models import UserProfile, WellnessLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'reminder_hour']

@admin.register(WellnessLog)
class WellnessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'water_intake_ml', 'exercise_type', 'exercise_duration', 'sleep_hours', 'mood']
    list_filter = ['date', 'mood']
    search_fields = ['user__username', 'mood', 'exercise_type']
