from django import forms
from .models import Appointment, Service, Master


class BookingForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='✂️ Выберите услугу',
        empty_label='-- Выберите услугу --'
    )
    
    master = forms.ModelChoiceField(
        queryset=Master.objects.filter(is_available=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='👤 Выберите мастера',
        empty_label='-- Выберите мастера --',
        required=False
    )
    
    datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label='🕐 Дата и время'
    )
    
    comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Пожелания, аллергия, особенности...'
        }),
        required=False,
        label='💬 Комментарии'
    )
    
    class Meta:
        model = Appointment
        fields = ['service', 'master', 'datetime', 'comments']
    
    def __init__(self, *args, **kwargs):
        master_id = kwargs.pop('master_id', None)
        super().__init__(*args, **kwargs)
        
        if master_id:
            try:
                master = Master.objects.get(id=master_id, is_available=True)
                
                # Скрываем поле мастера
                self.fields['master'].widget = forms.HiddenInput()
                self.fields['master'].initial = master.id
                self.fields['master'].required = False
                
                # Фильтруем услуги по специализации
                spec = master.specialization.lower()
                if 'парикмахер' in spec or 'стилист' in spec:
                    self.fields['service'].queryset = Service.objects.filter(category='hair', is_active=True)
                elif 'маникюр' in spec or 'педикюр' in spec:
                    self.fields['service'].queryset = Service.objects.filter(category='nails', is_active=True)
                elif 'косметолог' in spec:
                    self.fields['service'].queryset = Service.objects.filter(category='cosmetics', is_active=True)
                elif 'массаж' in spec:
                    self.fields['service'].queryset = Service.objects.filter(category='massage', is_active=True)
                    
            except Master.DoesNotExist:
                pass