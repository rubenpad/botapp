"""Define task to run with celery"""
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')
app.conf.timezone = 'America/Bogota'


@app.task()
def greeting(name):
    print(f'Hello, {name}')
