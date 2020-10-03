from django.db import models

# Create your models here.

class Pet(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    name = models.TextField(max_length=64, null=True)
    species = models.TextField(max_length=128, null=True)
    color = models.TextField(max_length=128, null=True)
    birth_date = models.DateField()
    gender = models.TextField(max_length=10, null=True)
    chip = models.TextField(max_length=64, null=True)
    avatar = models.ImageField(upload_to='pavatars/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"
        
