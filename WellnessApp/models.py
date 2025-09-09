from django.db import models
from datetime import date

from django.contrib.auth.models import User
MOOD_CHOICES = [
    ('Happy', 'Happy'),
    ('Neutral', 'Neutral'),
    ('Sad', 'Sad'),
]

EXERCISE_MET = {
    'Walking': 'Walking',
    'Jogging': 'Jogging',
    'Running': 'Running',
    'Cycling': 'Cycling',
    'Swimming': 'Swimming',
    'Gym': 'Gym',
    'Yoga': 'Yoga',
}

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    calorie_goal = models.PositiveIntegerField(default=300)
    reminder_hour = models.TimeField(default='09:00')

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class WellnessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    water_intake_ml = models.FloatField(null=True, blank=True)
    exercise_type = models.CharField(max_length=100,choices= EXERCISE_MET, blank=True)
    exercise_duration = models.PositiveIntegerField(null=True, blank=True)
    sleep_hours = models.FloatField(null=True, blank=True)
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES, blank=True)
    mood_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
