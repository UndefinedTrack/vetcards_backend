from django.db import models

# Create your models here.

class Procedure(models.Model):
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE, verbose_name='Питомец')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Ветеринар')
    purpose = models.TextField(max_length=128, null=True, verbose_name='Цель')
    symptoms = models.TextField(max_length=256, null=True, blank=True, verbose_name='Симптомы')
    diagnosis = models.TextField(max_length=256, null=True, blank=True, verbose_name='Диагноз')
    recomms = models.TextField(max_length=256, null=True, blank=True, verbose_name='Рекомендации')
    recipe = models.TextField(max_length=256, null=True, blank=True, verbose_name='Рецепт')
    proc_date = models.DateField(null=True, auto_now_add=True, verbose_name='Дата')
    
    class Meta:
        verbose_name = "Процедура"
        verbose_name_plural = "Процедуры"
        
class OwnerProcedure(models.Model):
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE, verbose_name='Питомец')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.TextField(max_length=128, null=True, verbose_name='Цель')
    description = models.TextField(max_length=256, null=True, blank=True, verbose_name='Описание')
    proc_date = models.DateField(null=True, auto_now_add=True, verbose_name='Дата')
    
    class Meta:
        verbose_name = "Домашняя процедура"
        verbose_name_plural = "Домашние процедуры"