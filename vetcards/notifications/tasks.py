from __future__ import absolute_import, unicode_literals

import datetime
from dateutil.relativedelta import relativedelta

from django.core.mail import EmailMessage, send_mail

from application.celery import app
from django.apps import apps

@app.task(bind=True)
def notif_sender():

    User = apps.get_model('users.User')
    Pet = apps.get_model('pets.Pet')
    Notification = apps.get_model('notifications.Notification')

    notifications = Notification.objects.all()

    today = datetime.date.today()

    for notif in notifications:

        diff = relativedelta(today, notif.notif_date)

        if notif.repeat == 'Раз в день':
            if diff.days == 1:
                message = EmailMessage(
                    'Количество пользователей',
                    'Необходимо провести процедуру: ' + notif.notif_type + ' питомцу ' + notif.pet.name + '. Описание процедуры: ' + notif.description + '.',
                    'undefined.track@gmail.com',
                    [notif.user.email],
                )
                
                message.send()

                notif.notif_date = today
                notif.save()

                continue
        elif notif.repeat == 'Раз в неделю':
            if diff.days == 7:
                message = EmailMessage(
                    'Количество пользователей',
                    'Необходимо провести процедуру: ' + notif.notif_type + ' питомцу ' + notif.pet.name + '. Описание процедуры: ' + notif.description + '.',
                    'undefined.track@gmail.com',
                    [notif.user.email],
                )
                
                message.send()

                notif.notif_date = today
                notif.save()

                continue
        elif notif.repeat == 'Раз в год':
            if diff.years == 1:
                message = EmailMessage(
                    'Количество пользователей',
                    'Необходимо провести процедуру: ' + notif.notif_type + ' питомцу ' + notif.pet.name + '. Описание процедуры: ' + notif.description + '.',
                    'undefined.track@gmail.com',
                    [notif.user.email],
                )
                
                message.send()

                notif.notif_date = today
                notif.save()

                continue