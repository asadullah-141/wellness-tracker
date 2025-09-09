from django import forms
from .models import UserProfile, WellnessLog
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

EXERCISE_MET_VALUES = {
    'Walking': 3.5,
    'Jogging': 7.0,
    'Running': 9.8,
    'Cycling': 6.0,
    'Swimming': 8.0,
    'Gym': 5.0,
    'Yoga': 2.5,
}

# ---------------------------
# 1. Calorie Burn Form
# ---------------------------
class CalorieBurnForm(forms.Form):
    exercise_type = forms.ChoiceField(
        choices=[(k, k) for k in EXERCISE_MET_VALUES.keys()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    duration = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'})
    )

# ---------------------------
# 2. Profile Update Form
# ---------------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'gender', 'date_of_birth', 'weight_kg', 'calorie_goal', 'reminder_hour']  # <- Added here
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'calorie_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'reminder_hour': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),  # <- Added
        }
        labels = {
            'calorie_goal': 'Daily Calorie Burn Goal (kcal)',
            'date_of_birth': 'Date of Birth',
            'reminder_hour': 'Daily Reminder Time',  # <- Added
        }

# ---------------------------
# 3. Reminder Time Form (Now Separate)
# ---------------------------
class ReminderTimeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['reminder_hour']
        widgets = {
            'reminder_hour': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        labels = {
            'reminder_hour': 'Daily Reminder Time'
        }

# ---------------------------
# 4. Password Change Form
# ---------------------------
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# ---------------------------
# 5. Wellness Log Form
# ---------------------------
class WellnessLogForm(forms.ModelForm):
    class Meta:
        model = WellnessLog
        fields = ['water_intake_ml', 'exercise_type', 'exercise_duration', 'sleep_hours', 'mood', 'mood_note']
        widgets = {
            'water_intake_ml': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Enter water in liters'
            }),
            'mood_note': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'exercise_type': forms.Select(attrs={'class': 'form-control'}),
            'exercise_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'water_intake_ml': 'Water Intake (liters)',
        }

    def clean_water_intake_ml(self):
        water = self.cleaned_data.get('water_intake_ml')
        if water is not None and water < 0:
            raise forms.ValidationError("Water intake must be a positive number.")
        return water

# ---------------------------
# 6. Registration Form
# ---------------------------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
