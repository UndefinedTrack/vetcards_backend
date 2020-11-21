from django.db import models

# Create your models here.

class Procedure(models.Model):
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE, verbose_name='Питомец')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Ветеринар')
    purpose = models.TextField(max_length=128, null=True, verbose_name='Цель')
    name = models.TextField(max_length=128, null=True, verbose_name='Название')
    symptoms = models.TextField(max_length=256, null=True, default='', blank=True, verbose_name='Симптомы')
    diagnosis = models.TextField(max_length=256, null=True, default='', blank=True, verbose_name='Диагноз')
    recomms = models.TextField(max_length=256, null=True, default='', blank=True, verbose_name='Рекомендации')
    recipe = models.TextField(max_length=256, null=True, default='', blank=True, verbose_name='Рецепт')
    proc_date = models.DateField(verbose_name='Дата')
    
    class Meta:
        verbose_name = "Процедура"
        verbose_name_plural = "Процедуры"
        
class OwnerProcedure(models.Model):
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE, verbose_name='Питомец')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.TextField(max_length=128, null=True, verbose_name='Цель')
    description = models.TextField(max_length=256, null=True, default='', blank=True, verbose_name='Описание')
    proc_date = models.DateField(verbose_name='Дата')
    
    class Meta:
        verbose_name = "Домашняя процедура"
        verbose_name_plural = "Домашние процедуры"

def vproc_att_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'attachments/vetprocs/{instance.proc.id}/{instance.id}.{ext}'

class VetAttachment(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    proc = models.ForeignKey(to=Procedure, on_delete=models.CASCADE)
    url = models.ImageField(upload_to=vproc_att_directory_path, verbose_name='Фотография')
    
    class Meta:
        verbose_name = 'Вложение Ветеринар'
        verbose_name_plural = 'Вложения Ветеринар'

def oproc_att_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'attachments/ownerprocs/{instance.proc.id}/{instance.id}.{ext}'

class OwnerAttachment(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    proc = models.ForeignKey(to=OwnerProcedure, on_delete=models.CASCADE)
    url = models.ImageField(upload_to=oproc_att_directory_path, verbose_name='Фотография')
    
    class Meta:
        verbose_name = 'Вложение Владелец'
        verbose_name_plural = 'Вложения Владелец'