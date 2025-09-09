#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from django.utils.timezone import now
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from .models import *

EXERCISE_MET_VALUES = {
    'Walking': 3.5,
    'Jogging': 7.0,
    'Running': 9.8,
    'Cycling': 6.0,
    'Swimming': 8.0,
    'Gym': 5.0,
    'Yoga': 2.5,
}

@login_required
def calorie_burn_view(request):
    result = None
    chart_data = []
    form = CalorieBurnForm()

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    weight = profile.weight_kg or 0
    goal = profile.calorie_goal or 0
    if weight <= 0:
        messages.warning(request, "Please enter your weight in the Profile section to calculate calories.")
        return redirect('profile')  # Redirects to profile before form even loads

    if request.method == 'POST':
        form = CalorieBurnForm(request.POST)
        if form.is_valid():
            ex_type = form.cleaned_data['exercise_type']
            duration = form.cleaned_data['duration']
            met = EXERCISE_MET_VALUES[ex_type]
            calories = met * weight * (duration / 60)
            result = {
                'exercise': ex_type,
                'duration': duration,
                'calories': round(calories, 2),
                'goal': goal,
                'progress': round((calories / goal) * 100) if goal else 0
            }

            # build chart data
            chart_data = [
                {
                    'exercise': ex,
                    'calories': round(m * weight * (duration / 60), 1)
                }
                for ex, m in EXERCISE_MET_VALUES.items()
            ]

    return render(request, 'WellnessApp/calorie_burn.html', {
        'form': form,
        'result': result,
        'chart_data': chart_data
    })


'''def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Password has been updated successfully!')

        return redirect('dashboard')
    else:
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'WellnessApp/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
'''
@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
            password_form = CustomPasswordChangeForm(request.user)  # Re-initialize blank
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            profile_form = ProfileUpdateForm(instance=profile)  # Re-initialize blank
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
                return redirect('profile')
        else:
            profile_form = ProfileUpdateForm(instance=profile)
            password_form = CustomPasswordChangeForm(request.user)
    else:
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'WellnessApp/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
    
    
#Landing View
def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'WellnessApp/landing.html')

# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'WellnessApp/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            #messages.error(request, 'Invalid username or password.')
            form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'WellnessApp/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard
'''@login_required
def dashboard(request):
    logs_all = WellnessLog.objects.filter(user=request.user).order_by('-date', '-time')
    paginator = Paginator(logs_all, 7)  # Show 7 logs per page
    page_number = request.GET.get('page')
    page_logs = paginator.get_page(page_number)

    # 7 most recent for charts
    chart_data = logs_all[:7][::-1]  # reverse for chronological display on chart

    return render(request, 'WellnessApp/dashboard.html', {
        'logs': page_logs,
        'chart_data': chart_data,
    })'''

@login_required
def dashboard(request):
    search_date = request.GET.get('date')
    logs_all = WellnessLog.objects.filter(user=request.user).order_by('-date', '-time')

    # Reorder: searched date log(s) first
    if search_date:
        try:
            search_date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
            matching = logs_all.filter(date=search_date_obj)
            others = logs_all.exclude(date=search_date_obj)
            logs_all = list(matching) + list(others)
        except:
            pass

    paginator = Paginator(logs_all, 7)
    page_number = request.GET.get('page')
    page_logs = paginator.get_page(page_number)

    chart_data = WellnessLog.objects.filter(user=request.user).order_by('-date', '-time')[:7][::-1]

    return render(request, 'WellnessApp/dashboard.html', {
        'logs': page_logs,
        'chart_data': chart_data,
        'search_date': search_date or ''
    })

# Add Log
@login_required
def add_log(request):
    if request.method == 'POST':
        form = WellnessLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Log added successfully!')
            return redirect('dashboard')
    else:
        form = WellnessLogForm()
    return render(request, 'WellnessApp/log_form.html', {'form': form})

# Edit Log
@login_required
def edit_log(request, pk):
    log = get_object_or_404(WellnessLog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WellnessLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Log updated successfully!')
            return redirect('dashboard')
    else:
        form = WellnessLogForm(instance=log)
    return render(request, 'WellnessApp/log_form.html', {'form': form})

# Delete Log
@login_required
def delete_log(request, pk):
    log = get_object_or_404(WellnessLog, pk=pk, user=request.user)
    log.delete()
    messages.success(request, 'Log deleted successfully!')
    return redirect('dashboard')


@login_required
def summary_report(request):
    period = request.GET.get('period', 'week')  # default to weekly
    count = 7 if period == 'week' else 30

    logs = WellnessLog.objects.filter(user=request.user).order_by('-date')[:count]

    avg_water = logs.aggregate(avg=Avg('water_intake_ml'))['avg'] or 0
    avg_sleep = logs.aggregate(avg=Avg('sleep_hours'))['avg'] or 0
    total_exercise = logs.aggregate(avg=Avg('exercise_duration'))['avg'] or 0

    mood_counts = logs.values('mood').annotate(count=Count('mood'))

    mood_data = {'Happy': 0, 'Neutral': 0, 'Sad': 0}
    for mood in mood_counts:
        mood_data[mood['mood']] = mood['count']

    context = {
        'avg_water': round(avg_water, 2),
        'avg_sleep': round(avg_sleep, 1),
        'total_exercise': int(total_exercise),
        'mood_data': mood_data,
        'period': period,
        'logs': logs  # optional, for count/debug
    }
    return render(request, 'WellnessApp/summary_report.html', context)