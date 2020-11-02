import datetime
from typing import Callable, Dict, List
from apscheduler import triggers
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
import pytz

class Task:
    registered_tasks: List['Task'] = []

    @classmethod
    def add_task(cls, *args, **kwargs):
        cls.registered_tasks.append(Task(*args, **kwargs))

    def __init__(self, func: Callable, trigger: IntervalTrigger,  *args, **kwargs) -> None:
        self.func = func
        self.trigger = trigger

def weekly_task(week_day: int, **timedelta_kwargs):
    """week_day of 0 means Monday"""

    def decorator(func):
        # Calculate time until expected date and time
        est = pytz.timezone('US/Eastern')

        today = datetime.datetime.today().astimezone(est).date()
        start_of_week = today + datetime.timedelta(days=-today.weekday())

        scheduled_time = datetime.datetime.combine(start_of_week, datetime.datetime.min.time()) + datetime.timedelta(days=week_day, **timedelta_kwargs)
        Task.add_task(func=func, run_time=scheduled_time, trigger=DateTrigger(scheduled_time, est))
        print(f"Scheduled task for {scheduled_time}")

    return decorator

