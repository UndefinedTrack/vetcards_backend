# Generated by Django 3.1.2 on 2020-10-20 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_auto_20201013_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='breed',
            field=models.TextField(blank=True, max_length=128, null=True, verbose_name='Порода'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='chip',
            field=models.TextField(blank=True, max_length=64, null=True, verbose_name='Чип'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='color',
            field=models.TextField(blank=True, max_length=128, null=True, verbose_name='Окрас'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='gender',
            field=models.TextField(blank=True, max_length=10, null=True, verbose_name='Пол'),
        ),
    ]
