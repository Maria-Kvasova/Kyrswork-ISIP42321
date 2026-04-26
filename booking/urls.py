from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/', views.booking_view, name='booking'),
    path('profile/', views.profile_view, name='profile'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('services/', views.services_view, name='services'),
    path('masters/', views.masters_view, name='masters'),
]