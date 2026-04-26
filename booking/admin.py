from django.contrib import admin
from .models import ClientProfile, Master, Service, Appointment


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'phone')
    list_filter = ('created_at',)


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'rating', 'is_available')
    search_fields = ('full_name', 'specialization')
    list_filter = ('is_available', 'specialization')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'category', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_active')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'service', 'datetime', 'status')
    search_fields = ('client__user__username', 'master__full_name')
    list_filter = ('status', 'datetime')
    date_hierarchy = 'datetime'