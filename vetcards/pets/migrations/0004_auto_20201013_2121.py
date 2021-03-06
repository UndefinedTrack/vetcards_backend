# Generated by Django 3.1.2 on 2020-10-13 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pets', '0003_auto_20201003_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='breed',
            field=models.TextField(max_length=128, null=True, verbose_name='Порода'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='pavatars/', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='birth_date',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='chip',
            field=models.TextField(max_length=64, null=True, verbose_name='Чип'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='color',
            field=models.TextField(max_length=128, null=True, verbose_name='Окрас'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='gender',
            field=models.TextField(max_length=10, null=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='name',
            field=models.TextField(max_length=64, null=True, verbose_name='Кличка'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='species',
            field=models.TextField(max_length=128, null=True, verbose_name='Вид'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
