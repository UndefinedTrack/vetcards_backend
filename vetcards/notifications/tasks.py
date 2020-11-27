from __future__ import absolute_import, unicode_literals

import datetime
from dateutil.relativedelta import relativedelta

from django.core.mail import EmailMessage, send_mail

from application.celery import app
from django.apps import apps

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

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

    account = 'ACee25afae30abd5768967c38a5a0ce218'
    token = '1fff817fcc19b6bcc7270b30b19b9f53'

    phone = '+12058090690'

    client = Client(account, token)

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

                    uphone = '+7' + notif.user.phone[1:] if (not notif.user.phone is None) and notif.user.phone[0] == 8 else notif.user.phone

                    try:
                        msg = client.messages.create(to=uphone, 
                        from_=phone, 
                        body=body_temp)
                    except TwilioRestException as e:
                        print(e)

                    email_text = f'From: {sent_from}\nTo: {sent_to}\nSubject: {subject}\n\n{body_temp}'.encode('utf-8')
                    server_ssl.sendmail(sent_from, sent_to, email_text)

                    notif.notif_date = today
                    notif.save()

                    continue
            elif notif.repeat == 'Раз в неделю':
                if diff.days == 7 and diff.months == 0 and diff.years == 0:

                    uphone = '+7' + notif.user.phone[1:] if (not notif.user.phone is None) and notif.user.phone[0] == 8 else notif.user.phone

                    try:
                        msg = client.messages.create(to=uphone, 
                        from_=phone, 
                        body=body_temp)
                    except TwilioRestException as e:
                        print(e)

                    email_text = f'From: {sent_from}\nTo: {sent_to}\nSubject: {subject}\n\n{body_temp}'.encode('utf-8')
                    server_ssl.sendmail(sent_from, sent_to, email_text)

                    notif.notif_date = today
                    notif.save()

                    continue
            elif notif.repeat == 'Раз в год':
                if diff.years == 1 and diff.months == 0 and diff.days == 0:

                    uphone = '+7' + notif.user.phone[1:] if (not notif.user.phone is None) and notif.user.phone[0] == 8 else notif.user.phone

                    try:
                        msg = client.messages.create(to=uphone, 
                        from_=phone, 
                        body=body_temp)
                    except TwilioRestException as e:
                        print(e)

                    email_text = f'From: {sent_from}\nTo: {sent_to}\nSubject: {subject}\n\n{body_temp}'.encode('utf-8')
                    server_ssl.sendmail(sent_from, sent_to, email_text)

                    notif.notif_date = today
                    notif.save()

                    continue
        server_ssl.close()
    except Exception as exc:
        print(str(exc))


@app.task()
def broadcast_notif(address, subject, message):

    gmail_login = 'undefined.track@gmail.com'
    gmail_password = 'elnylnlttmxavzwm'
    sent_from = gmail_login

    account = 'ACee25afae30abd5768967c38a5a0ce218'
    token = '1fff817fcc19b6bcc7270b30b19b9f53'

    phone = '+12058090690'
    
    User = apps.get_model('users.User')

    client = Client(account, token)

    users = User.objects.filter(region=address["region"], city=address["city"], street=address["street"])

    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(gmail_login, gmail_password)

        for user in users:
            sent_to = user.email
            body_temp = f'Уважаемый(ая), {user.first_name} {user.patronymic}\n {message}'

            email_text = f'From: {sent_from}\nTo: {sent_to}\nSubject: {subject}\n\n{body_temp}'.encode('utf-8')
            server_ssl.sendmail(sent_from, sent_to, email_text)

            uphone = '+7' + user.phone[1:] if (not user.phone is None) and user.phone[0] == 8 else user.phone

            try:
                msg = client.messages.create(to=uphone, 
                from_=phone, 
                body=body_temp)
            except TwilioRestException as e:
                print(e)


    except Exception as exc:
        print(str(exc))
