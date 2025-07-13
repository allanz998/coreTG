import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_tg.settings')
app = Celery('django_tg')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() 
