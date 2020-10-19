from django.db import models

# Create your models here.

class Slot(models.Model):
    vet = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Ветеринар')
    slot_date = models.DateField(verbose_name='Время')
    slot_time = models.TimeField(verbose_name='Дата')
    purpose = models.TextField(max_length=128, null=True, blank=True, verbose_name='Цель')
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Питомец')
    appointed = models.BooleanField(default=False, blank=True, verbose_name='Занято')

    class Meta:
        verbose_name = "Слот"
        verbose_name_plural = "Слоты"