from django.db import models

# Create your models here.

class Pet(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.TextField(max_length=64, null=True, verbose_name='Кличка')
    species = models.TextField(max_length=128, null=True, verbose_name='Вид')
    color = models.TextField(max_length=128, null=True, verbose_name='Окрас')
    birth_date = models.DateField(verbose_name='Дата рождения')
    gender = models.TextField(max_length=10, null=True, verbose_name='Пол')
    chip = models.TextField(max_length=64, null=True, verbose_name='Чип')
    avatar = models.ImageField(upload_to='pavatars/', null=True, blank=True, verbose_name='Фотография')
    
    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"
        
