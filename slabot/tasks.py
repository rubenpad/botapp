"""Define task to run with celery"""
import os
from celery import Celery

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

app = Celery('tasks', broker=CELERY_BROKER_URL)
app.conf.timezone = 'America/Bogota'


@app.task(name='greeting')
def greeting(name):
    print(f'Hello, {name}')
