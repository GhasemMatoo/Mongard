import logging
from functools import partial, update_wrapper
from datetime import timedelta, datetime
from collections.abc import Hashable

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

    def run_pending(self):
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            self._run_job(job)

    @staticmethod
    def _run_job(job):
        job.run()

    def get_jobs(self, tag=None):
        if tag is None:
            return self.jobs[:]
        else:
            return [job for job in self.jobs if tag in job.tags]

    def get_next_run(self, tag=None):
        if not self.jobs:
            return None
        jobs_filtered = self.get_jobs(tag)
        if not jobs_filtered:
            return None
        return min(jobs_filtered).next_run
    next_run = property(get_next_run)

    @property
    def idle_seconds(self):
        if not self.next_run:
            return None
        return (self.next_run - datetime.now()).total_seconds()


class Job:

    def __init__(self, interval, scheduler):
        self.interval = interval
        self.job_func = None
        self.unit = None
        self.period = None
        self.last_run = None
        self.next_run = None
        self.tags = set()
        self.scheduler = scheduler
        self._unit_tuple = ('seconds', 'minutes', 'hours', 'days', 'weeks')

    def __lt__(self, other):
        return self.next_run < other.next_run

    @property
    def second(self):
        if self.interval != 1:
            raise IntervalError("Use seconds instead of second")
        return self.seconds

    @property
    def seconds(self):
        self.unit = 'seconds'
        return self
    
    @property
    def minute(self):
        if self.interval != 1:
            raise IntervalError("Use seconds instead of minute")
        return self.minute

    @property
    def minutes(self):
        self.unit = 'minutes'
        return self
    
    @property
    def hour(self):
        if self.interval != 1:
            raise IntervalError("Use seconds instead of hour")
        return self.hours

    @property
    def hours(self):
        self.unit = 'hours'
        return self

    @property
    def day(self):
        if self.interval != 1:
            raise IntervalError("Use seconds instead of day")
        return self.days

    @property
    def days(self):
        self.unit = 'days'
        return self

    @property
    def week(self):
        if self.interval != 1:
            raise IntervalError("Use seconds instead of week")
        return self.weeks

    @property
    def weeks(self):
        self.unit = 'weeks'
        return self

    def tag(self, *tags):
        if not all(isinstance(tag, Hashable)for tag in tags):
            raise TypeError("Tags must be hashable")
        self.tags.update(tags)
        return self

    def do(self, job_func, *arg, **kwargs):
        self.job_func = partial(job_func, *arg, **kwargs)
        update_wrapper(self.job_func, job_func)
        if self.job_func is None:
            raise SchedulerError("Unable to add job to scheduler ")
        self._scheduler_next_run()
        self.scheduler.jobs.append(self)
        return self

    def should_run(self):
        assert self.next_run is not None, 'must run _scheduler_next_run before'
        return self.next_run <= datetime.now()

    def run(self):
        logger.debug(f'Running job {self}')
        ret = self.job_func()
        self.last_run = datetime.now()
        self._scheduler_next_run()
        return ret

    def _scheduler_next_run(self):
        if self.unit not in self._unit_tuple:
            raise SchedulerValueError(
                f"Invalid unit (valid units are {self._unit_tuple})"
            )
        interval = self.interval
        self.period = timedelta(**{self.unit: self.interval})
        self.next_run = datetime.now() + self.period


default_scheduler = Scheduler()


def every(interval=1):
    return default_scheduler.every(interval)


def run_pending():
    return default_scheduler.run_pending()


def get_jobs(tag=None):
    return default_scheduler.get_jobs(tag)


def get_next_run(tag=None):
    return default_scheduler.get_next_run(tag)


def idle_seconds():
    return default_scheduler.idle_seconds
