import logging
from functools import partial, update_wrapper

logger = logging.getLogger('schedule')


class SchedulerError(Exception):
    """Base schedule exception"""


class SchedulerValueError(SchedulerError):
    """Base schedule value error"""


class IntervalError(SchedulerError):
    """An improper interval was used"""


class Scheduler:
    def __init__(self):
        self.jobs = []

    def every(self, interval):
        job = Job(interval, self)
        return job


class Job:

    def __init__(self, interval, scheduler):
        self.interval = interval
        self.job_func = None
        self.unit = None
        self.scheduler = scheduler

    @property
    def second(self):
        if self.interval != 1:
            raise IntervalError("Use seconds instead of second")
        return self.seconds

    @property
    def seconds(self):
        self.unit = 'seconds'
        return self

    def do(self, job_func, *arg, **kwargs):
        self.job_func = partial(job_func, *arg, **kwargs)
        update_wrapper(self.job_func, job_func)
        self._scheduler_next_run()
        if self.job_func is None:
            raise SchedulerError("Unable to add job to scheduler ")
        self.scheduler.jobs.append(self)
        return self

    def _scheduler_next_run(self):
        pass


default_scheduler = Scheduler()


def every(interval=1):
    default_scheduler.every(interval)

