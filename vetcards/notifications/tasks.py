from __future__ import absolute_import, unicode_literals

from application.celery import app
from django.apps import apps

@app.task(bind=True)
def notif_sender():
    pass