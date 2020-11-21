from django.db import models

# Create your models here.

def avatar_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'pavatars/{instance.user.id}_{instance.id}.{ext}'

class Pet(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.TextField(max_length=64, null=True, verbose_name='Кличка')
    species = models.TextField(max_length=128, null=True, verbose_name='Вид')
    breed = models.TextField(max_length=128, null=True, blank=True, verbose_name='Порода')
    color = models.TextField(max_length=128, null=True, blank=True, verbose_name='Окрас')
    birth_date = models.TextField(max_length=10, null=True, blank=True, verbose_name='Дата рождения')
    gender = models.TextField(max_length=10, null=True, blank=True, verbose_name='Пол')
    chip = models.TextField(max_length=64, null=True, blank=True, verbose_name='Чип')
    sterilized = models.BooleanField(default=False, verbose_name='Кастрирован/Стерилизована')
    vaccinated = models.BooleanField(default=False, verbose_name='Привит(а)')
    contraindications = models.TextField(max_length=512, null=True, blank=True, verbose_name='Противопоказания')
    notes = models.TextField(max_length=512, null=True, blank=True, verbose_name='Особые пометки')
    weight = models.FloatField(default=0, blank=True, verbose_name='Вес')
    avatar = models.ImageField(upload_to=avatar_directory_path, null=True, blank=True, verbose_name='Фотография')
    #avatar = models.ImageField(upload_to='pavatars/', null=True, blank=True, verbose_name='Фотография')
    
    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"
        
