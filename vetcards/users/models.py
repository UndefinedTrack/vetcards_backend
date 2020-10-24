from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def avatar_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'uavatars/{instance.id}.{ext}'

class User(AbstractUser):
    patronymic = models.TextField(max_length=64, null=True, blank=True, verbose_name='Отчество')
    phone = models.TextField(max_length=64, null=True, blank=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to=avatar_directory_path, null=True, blank=True, verbose_name='Фотография')
    vet = models.BooleanField(default=False, verbose_name='Ветеринар')
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
