from django.db import models

# Create your models here.

class Notification(models.Model):
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE, verbose_name='Питомец')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    notif_type = models.TextField(max_length=128, null=True, verbose_name='Тип процедуры')
    description = models.TextField(max_length=128, null=True, blank=True, verbose_name='Описание')
    repeat = models.TextField(max_length=30, null=True, verbose_name='Повторять')
    notif_date = models.DateField(null=True, auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Напоминание"
        verbose_name_plural = "Напоминания"