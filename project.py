import logging
import re
from functools import partial, update_wrapper
from datetime import timedelta, datetime, time
from time import sleep
from collections.abc import Hashable

logger = logging.getLogger('schedule')


class SchedulerError(Exception):
    """Base schedule exception"""


class SchedulerValueError(SchedulerError):
    """Base schedule value error"""


class IntervalError(SchedulerError):
    """An improper interval was used"""


class CancelJob:
    """
    Cancel job; can be returned from a job to unschedule itself.
    """


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

    def _run_job(self, job):
        result = job.run()
        if isinstance(result, CancelJob) or result is CancelJob:
            self.cancel_job(job)

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

    def clear(self, tag=None):
        if not tag:
            logger.debug(f'Deleting all jobs')
            del self.jobs[:]
        else:
            logger.debug(f'Deleting all jobs in tagged {tag}')
            self.jobs[:] = (job for job in self.jobs if tag not in job.tags)

    def run_all(self, delay_seconds=0):
        logger.debug(f'Running all {len(self.jobs)} jobs with {delay_seconds} delay in between')
        for job in self.jobs[:]:
            sleep(delay_seconds)
            self._run_job(job)

    def cancel_job(self, job):
        try:
            logger.debug(f'Canceling job {str(job)}')
            self.jobs.remove(job)
        except ValueError:
            logger.debug(f'Canceling not scheduled list job {str(job)}')


class Job:

    def __init__(self, interval, scheduler):
        self.interval = interval
        self.job_func = None
        self.unit = None
        self.period = None
        self.last_run = None
        self.next_run = None
        self.cancel_after = None
        self.latest = None
        self.start_day = None
        self.at_time = None
        self.at_time_zone = None
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

    @property
    def monday(self):
        if self.interval != 1:
            raise IntervalError(
                'Scheduling .monday() job is only allowed for weekly jobs.'
                'Using .monday() on a job scheduled to tun every 2 or more weeks'
                'is ont supported'
            )
        self.start_day = 'monday'
        return self.weeks

    def to(self, latest):
        self.latest = latest
        return self

    def at(self, time_str, tz=None):
        if self.unit not in ('days', 'hours', 'minutes') and not self.start_day:
            raise SchedulerValueError(
                "Invalid unit (valid units are `days`, `hours`, and `minutes`"
            )

        if tz is not None:
            from pytz import timezone, BaseTzInfo

            if isinstance(tz, str):
                self.at_time_zone = timezone(tz)
            elif isinstance(tz, BaseTzInfo):
                self.at_time_zone = tz
            else:
                raise SchedulerValueError("Timezone must be sting or pytz.timezone object")

        if not isinstance(time_str, str):
            raise TypeError("at() should be passed a string ")

        if self.unit == 'days' or self.start_day:
            if not re.match(r'^[0-2]\d:[0-5]\d(:[0-5]\d)?$', time_str):
                raise SchedulerValueError("Invalid time format for a daily job (valid format is HH:MM(:SS)?)")

        if self.unit == 'hours':
            if not re.match(r'^([0-5]\d)?:[0-5]\d$', time_str):
                raise SchedulerValueError("Invalid time format for a hourly job (valid format is (MM)?:ss)")

        if self.unit == 'minutes':
            if not re.match(r'^:[0-5}\d$]', time_str):
                raise SchedulerValueError("Invalid time format for a minutes job (valid format is :SS)")
        time_values = time_str.split(':')

        if len(time_values) == 3:
            hour, minute, second = time_values
        elif len(time_values) == 2 and self.unit == 'minutes':
            hour, minute = 0, 0
            _, second = time_values
        elif len(time_values) == 2 and self.unit == 'hours' and len(time_values[0]):
            hour = 0
            minute, second = time_values
        else:
            hour, minute = time_values
            second = 0

        if self.unit == 'days' or self.start_day:
            hour = int(hour)
            if not (0 <= hour <= 23):
                raise SchedulerValueError("Invalid number of hours ({} is not between 0 and 23)")
        elif self.unit == 'hours':
            hour = 0
        elif self.unit == 'minutes':
            hour, minute = 0, 0

        hour = int(hour)
        minute = int(minute)
        second = int(second)
        self.at_time = time(hour, minute, second)
        return  self

    @staticmethod
    def _decode_datetime_str(datetime_str, formats_str):
        for format_time in formats_str:
            try:
                return datetime.strptime(datetime_str, format_time)
            except ValueError:
                pass
        return None

    def until(self, until_time):
        if isinstance(until_time, datetime):
            self.cancel_after = until_time
        elif isinstance(until_time, timedelta):
            self.cancel_after = datetime.now() + until_time
        elif isinstance(until_time, time):
            self.cancel_after = datetime.combine(datetime.now(), until_time)
        elif isinstance(until_time, str):
            cancel_after = self._decode_datetime_str(
                until_time,
                [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d %H:%M',
                    '%H:%M:%S',
                    '%H:%M'
                ]
            )
            if cancel_after is None:
                raise SchedulerValueError("Invalid string format for until(import time)")
            if '-' not in until_time:
                date_time_now = datetime.now()
                cancel_after = cancel_after.replace(
                    year=date_time_now.year, month=date_time_now.month, day=date_time_now.day
                )
            self.cancel_after = cancel_after
        else:
            raise TypeError(
                'until() takes a string, datetime.datetime, datatime.timedelta,'
                'datetime.time parameter valid'
            )
        if self.cancel_after < datetime.now():
            raise SchedulerValueError(
                'Cannot scheduler a job to run until a time in the past'
            )
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

    def _is_overdue(self, time_new):
        return self.cancel_after is not None and time_new > self.cancel_after

    def run(self):
        if self._is_overdue(datetime.now()):
            logger.debug(f'Cancelling job {self}')
            return CancelJob

        logger.debug(f'Running job {self}')
        ret = self.job_func()
        self.last_run = datetime.now()
        self._scheduler_next_run()
        if self._is_overdue(self.next_run):
            logger.debug(f'Cancelling job {self}')
            return CancelJob

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


def repeat(job, *arg, **kwargs):
    def _scheduler_decorator(decorator_function):
        job.do(decorator_function, *arg, **kwargs)
        return decorator_function
    return _scheduler_decorator


def clear(tag=None):
    default_scheduler.clear(tag)


def run_all(delay_seconds=None):
    default_scheduler.run_all(delay_seconds=delay_seconds)


def cancel_job(job):
    default_scheduler.cancel_job(job)
