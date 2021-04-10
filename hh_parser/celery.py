import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hh_parser.settings')

app = Celery('hh_parser', broker='redis://redis:6379')
app.conf.result_backend = 'redis://redis:6379/0'

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
