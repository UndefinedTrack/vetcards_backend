# Generated by Django 3.1.2 on 2020-11-23 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_notif_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='description',
            field=models.TextField(blank=True, max_length=128, null=True, verbose_name='Описание'),
        ),
    ]
