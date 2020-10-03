from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    patronymic = models.TextField(max_length=64, null=True, blank=True)
    phone = models.TextField(max_length=64, null=True)
    avatar = models.ImageField(upload_to='uavatars/', null=True, blank=True)
    vet = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
