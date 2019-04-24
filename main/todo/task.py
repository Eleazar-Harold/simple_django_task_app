from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from main.todo.models import Todo
from main.celery import app
from background_task import background

logger = get_task_logger(__name__)


@app.task
def cross_check_tasks():
    timehold = datetime.now() - timedelta(hours=5)
    tasks = Todo.objects.filter(taskdate__lte=timehold)
    if tasks:
        print(str(tasks.count) +' tasks to cross check found...')
        for task in tasks:
            if task.started == False:
                task.started = True
            task.save()
            print('task -->' + task.description + ' started')
    else:
        print('no available task to crosscheck')


@background(schedule=60)
def inline_task_checker(pk):
    timehold = datetime.now() - timedelta(hours=4)
    tasks = Todo.objects.filter(taskdate__lt=timehold, id=pk)
    for task in tasks:
        logger.info('checking task {0}'.format(task.description))
        if task.started == False:
            task.started = True
            task.save()
            print('task -->' + task.description + ' started')
    inline_task_expirer(pk)
        

@background(schedule=600)
def inline_task_expirer(pk):
    timehold = datetime.now() - timedelta(hours=4)
    try:
        tasks = Todo.objects.filter(taskdate__lt=timehold, id=pk)
        for task in tasks:
            print('execution task {}'.format(task.description))
            if task.complete == True:
                task.expire = True
            elif task.complete == False:
                task.expire = True
            task.save()
            print('task --> ' + task.description + ' expired')
    except (TypeError, ValueError, MemoryError, RuntimeError) as e:
        logger.error('task execution error: {}'.format(e))

     
@app.task
def expired_tasks(self):
    try:
        tasks = Todo.objects.filter(taskdate__lt=datetime.now())
        for task in tasks:
            print('execution task {}'.format(task.description))
            if task.complete == True:
                task.expire = True
            elif task.complete == False:
                task.expire = True
            task.save()
            print('task --> ' + task.description + ' expired')
    except (TypeError, ValueError, MemoryError, RuntimeError) as e:
        raise self.retry(exc=e) 

