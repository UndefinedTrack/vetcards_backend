from __future__ import absolute_import, unicode_literals

import datetime
from dateutil.relativedelta import relativedelta

from django.core.mail import EmailMessage, send_mail

from application.celery import app
from django.apps import apps

import smtplib

@app.task(bind=True)
def notif_sender(self):

    User = apps.get_model('users.User')
    Pet = apps.get_model('pets.Pet')
    Notification = apps.get_model('notifications.Notification')

    notifications = Notification.objects.all()

    today = datetime.date.today()

    gmail_login = 'undefined.track@gmail.com'
    gmail_password = 'elnylnlttmxavzwm'
    sent_from = gmail_login
    subject = 'Напоминание'

    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(gmail_login, gmail_password)

        for notif in notifications:

            diff = relativedelta(today, notif.notif_date)

            sent_to = notif.user.email
            body_temp = 'Необходимо провести процедуру: ' + notif.notif_type + ' питомцу ' + notif.pet.name + '. Описание процедуры: ' + notif.description + '.'

            if notif.repeat == 'Раз в день':
                if diff.days == 1 and diff.months == 0 and diff.years == 0:
                    '''message = EmailMessage(
                        'Напоминание',
                        'Необходимо провести процедуру: ' + notif.notif_type + ' питомцу ' + notif.pet.name + '. Описание процедуры: ' + notif.description + '.',
                        'undefined.track@gmail.com',
                        [notif.user.email],
                    )
                    
                    message.send()'''

                    email_text = f'From: {sent_from}\nTo: {sent_to}\nSubject: {subject}\n\n{body_temp}'.encode('utf-8')
                    server_ssl.sendmail(sent_from, sent_to, email_text)

                    notif.notif_date = today
                    notif.save()

                    continue
            elif notif.repeat == 'Раз в неделю':
                if diff.days == 7 and diff.months == 0 and diff.years == 0:
                    '''message = EmailMessage(
                        'Напоминание',
                        'Необходимо провести процедуру: ' + notif.notif_type + ' питомцу ' + notif.pet.name + '. Описание процедуры: ' + notif.description + '.',
                        'undefined.track@gmail.com',
                        [notif.user.email],
                    )
                    
                    message.send()'''

                    email_text = f'From: {sent_from}\nTo: {sent_to}\nSubject: {subject}\n\n{body_temp}'.encode('utf-8')
                    server_ssl.sendmail(sent_from, sent_to, email_text)

                    notif.notif_date = today
                    notif.save()

                    continue
            elif notif.repeat == 'Раз в год':
                if diff.years == 1 and diff.months == 0 and diff.days == 0:
                    '''message = EmailMessage(
                        'Напоминание',
                        'Необходимо провести процедуру: ' + notif.notif_type + ' питомцу ' + notif.pet.name + '. Описание процедуры: ' + notif.description + '.',
                        'undefined.track@gmail.com',
                        [notif.user.email],
                    )
                    
                    message.send()'''

                    email_text = f'From: {sent_from}\nTo: {sent_to}\nSubject: {subject}\n\n{body_temp}'.encode('utf-8')
                    server_ssl.sendmail(sent_from, sent_to, email_text)

                    notif.notif_date = today
                    notif.save()

                    continue
        server_ssl.close()
    except Exception as exc:
        print(str(exc))