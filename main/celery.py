from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main.todo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'tasks-expirer': {
        'task': 'main.todo.tasks.expired_tasks',
        'schedule': crontab(minute='*/15'), # crontab(minute=0, hour=0)
    },
    'tasks-crosschecker': {
        'task': 'main.todo.tasks.cross_check_tasks',
        'schedule': crontab(minute='*/3'),
    }
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
