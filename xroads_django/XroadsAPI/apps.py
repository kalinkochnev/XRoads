from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from .tasks import Task

class XroadsapiConfig(AppConfig):
    name = 'XroadsAPI'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.timezone = pytz.timezone('US/Eastern')

        for i, task in enumerate(Task.registered_tasks):
            print(i)
            scheduler.add_job(task.func, trigger=task.trigger, misfire_grace_time=99999)
        scheduler.start()


