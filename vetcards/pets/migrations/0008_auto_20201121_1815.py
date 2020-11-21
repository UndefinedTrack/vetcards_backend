# Generated by Django 3.1.2 on 2020-11-21 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0007_auto_20201027_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='contraindications',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='Противопоказания'),
        ),
        migrations.AddField(
            model_name='pet',
            name='notes',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='Особые пометки'),
        ),
        migrations.AddField(
            model_name='pet',
            name='sterilized',
            field=models.BooleanField(default=False, verbose_name='Кастрирован/Стерилизована'),
        ),
        migrations.AddField(
            model_name='pet',
            name='vaccinated',
            field=models.BooleanField(default=False, verbose_name='Привит(а)'),
        ),
        migrations.AddField(
            model_name='pet',
            name='weight',
            field=models.FloatField(blank=True, default=0, verbose_name='Вес'),
        ),
    ]
