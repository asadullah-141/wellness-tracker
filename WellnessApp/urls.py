# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_log, name='add_log'),
    path('edit/<int:pk>/', views.edit_log, name='edit_log'),
    path('delete/<int:pk>/', views.delete_log, name='delete_log'),
    path('summary/', views.summary_report, name='summary'),
    path('profile/', views.profile_view, name='profile'),
    path('calories/', views.calorie_burn_view, name='calorie_burn'),


]
