# Generated by Django 3.1.2 on 2020-11-16 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notif_type',
            field=models.TextField(max_length=128, null=True, verbose_name='Тип процедуры'),
        ),
    ]
