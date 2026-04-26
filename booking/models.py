from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ClientProfile(models.Model):
    """Профиль клиента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    notes = models.TextField(blank=True, verbose_name="Заметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профили клиентов"
    
    def __str__(self):
        return f"{self.user.username} - {self.phone}"


class Master(models.Model):
    """Мастер салона"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    specialization = models.CharField(max_length=50, verbose_name="Специализация")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Рейтинг")
    is_available = models.BooleanField(default=True, verbose_name="Доступен для записи")
    photo = models.ImageField(upload_to='masters/', null=True, blank=True, verbose_name="Фото")
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
    
    def __str__(self):
        return f"{self.full_name} - {self.specialization}"


class Service(models.Model):
    """Услуга салона"""
    CATEGORY_CHOICES = [
        ('hair', 'Парикмахерский зал'),
        ('nails', 'Маникюр/Педикюр'),
        ('cosmetics', 'Косметология'),
        ('massage', 'Массаж'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(blank=True, verbose_name="Описание")
    duration = models.IntegerField(help_text="Длительность в минутах", verbose_name="Длительность")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Appointment(models.Model):
    """Запись клиента"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
        ('no_show', 'Клиент не явился'),
    ]
    
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, 
                               verbose_name="Клиент", related_name='appointments')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, 
                               verbose_name="Мастер", related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, 
                                verbose_name="Услуга", related_name='appointments')
    datetime = models.DateTimeField(verbose_name="Дата и время")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                              default='pending', verbose_name="Статус")
    comments = models.TextField(blank=True, verbose_name="Комментарии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['-datetime']
    
    def __str__(self):
        return f"{self.client.user.username} - {self.service.name} - {self.datetime}"