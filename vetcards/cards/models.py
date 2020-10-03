from django.db import models

# Create your models here.

class Procedure(models.Model):
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE)
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    purpose = models.TextField(max_length=128, null=True)
    symptoms = models.TextField(max_length=256, null=True, blank=True)
    diagnosis = models.TextField(max_length=256, null=True, blank=True)
    recomms= models.TextField(max_length=256, null=True, blank=True)
    recipe = models.TextField(max_length=256, null=True, blank=True)
    proc_date = models.DateField(null=True, auto_now_add=True)
    
    class Meta:
        verbose_name = "Процедура"
        verbose_name_plural = "Процедуры"
        
class OwnerProcedure(models.Model):
    pet = models.ForeignKey(to='pets.Pet', on_delete=models.CASCADE)
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    name = models.TextField(max_length=128, null=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    proc_date = models.DateField(null=True, auto_now_add=True)
    
    class Meta:
        verbose_name = "Домашняя процедура"
        verbose_name_plural = "Домашние процедуры"