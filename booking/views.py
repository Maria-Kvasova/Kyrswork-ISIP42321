from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import BookingForm
from .models import Service, Master, Appointment, ClientProfile


# 🏠 ГЛАВНАЯ
def index(request):
    services = Service.objects.filter(is_active=True)[:6]
    masters = Master.objects.filter(is_available=True)[:4]
    return render(request, 'booking/index.html', {
        'services': services,
        'masters': masters
    })


# 📋 УСЛУГИ
def services_view(request):
    category = request.GET.get('category')
    if category:
        services = Service.objects.filter(category=category, is_active=True)
    else:
        services = Service.objects.filter(is_active=True)
    return render(request, 'booking/services.html', {'services': services})


# 👥 МАСТЕРА
def masters_view(request):
    masters = Master.objects.filter(is_available=True)
    return render(request, 'booking/masters.html', {'masters': masters})


# 📝 РЕГИСТРАЦИЯ
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ClientProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, '✅ Регистрация успешна!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})


# 🔐 ВХОД
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'✅ С возвращением, {user.username}!')
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'booking/login.html', {'form': form})


# 🚪 ВЫХОД
def logout_view(request):
    logout(request)
    messages.info(request, '👋 Вы вышли из системы')
    return redirect('index')


# 📅 ЗАПИСЬ (С master_id)
@login_required
def booking_view(request):
    master_id = request.GET.get('master_id')
    master = None
    
    if master_id:
        try:
            master = Master.objects.get(id=master_id, is_available=True)
        except Master.DoesNotExist:
            master = None
    
    ClientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, master_id=master_id)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user.clientprofile
            if not appointment.master and master_id:
                appointment.master_id = master_id
            appointment.save()
            messages.success(request, f'✅ Запись создана! Мастер: {appointment.master.full_name}')
            return redirect('profile')
    else:
        form = BookingForm(master_id=master_id)
    
    return render(request, 'booking/booking.html', {
        'form': form,
        'master': master
    })


# 👤 ПРОФИЛЬ
@login_required
def profile_view(request):
    ClientProfile.objects.get_or_create(user=request.user)
    now = timezone.now()
    upcoming = Appointment.objects.filter(
        client__user=request.user,
        datetime__gte=now
    ).order_by('datetime')
    history = Appointment.objects.filter(
        client__user=request.user,
        datetime__lt=now
    ).order_by('-datetime')
    profile = request.user.clientprofile
    return render(request, 'booking/profile.html', {
        'upcoming': upcoming,
        'history': history,
        'profile': profile
    })


# ❌ ОТМЕНА
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, client__user=request.user)
    if appointment.datetime > timezone.now() + timedelta(hours=2):
        appointment.delete()
        messages.success(request, '🗑️ Запись отменена')
    else:
        messages.error(request, '❌ Отмена возможна не менее чем за 2 часа')
    return redirect('profile')