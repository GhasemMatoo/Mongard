from unittest import TestCase, mock
from datetime import datetime
from scheduler import every, repeat, SchedulerError, SchedulerValueError, IntervalError
import scheduler


def make_mock_job(name=None):
    job = mock.Mock()
    job.__name__ = name or 'job'
    return job

class mock_datetime:
    def __init__(self, year, month, dey, hour, minute, second=0):
        self.year = year
        self.month = month
        self.dey = dey
        self.hour = hour
        self.minute = minute
        self.second = second
        self.original_datetime = None

    def __enter__(self):
        class MOckDate(datetime):
            @classmethod
            def today(cls):
                return cls(self.year, self.month, self.dey)

            @classmethod
            def now(cls, tz=None):
                return cls(self.year, self.month, self.dey, self.hour, self.minute, self.second)
        self.original_datetime = datetime
        datetime = MOckDate

    def __exit__(self, exc_type, exc_val, exc_tb):
        datetime = self.original_datetime


class SchedulerTest(TestCase):
    def setUp(self):
        scheduler.clear()

    def test_time_units(self):
        assert every().seconds.unit == 'seconds'
        assert every().minutes.unit == 'minutes'
        assert every().hours.unit == 'hours'
        assert every().days.unit == 'days'
        assert every().weeks.unit == 'weeks'

        job_instance = scheduler.Job(interval=2)

        with self.assertRaises(IntervalError):
            job_instance.second
        with self.assertRaises(IntervalError):
            job_instance.minute
        with self.assertRaises(IntervalError):
            job_instance.hour
        with self.assertRaises(IntervalError):
            job_instance.day
        with self.assertRaises(IntervalError):
            job_instance.week

        with self.assertRaisesRegex(
            IntervalError, (
                        r'Scheduling \.monday\(\) job is only allowed for weekly jobs\.'
                        r'Using \.monday\(\) on a job scheduled to tun every 2 or more weeks'
                        r'is ont supported'
                )
        ):
            job_instance.monday
        with self.assertRaisesRegex(
            IntervalError, (
                        r'Scheduling \.tuesday\(\) job is only allowed for weekly jobs\.'
                        r'Using \.tuesday\(\) on a job scheduled to tun every 2 or more weeks'
                        r'is ont supported'
                )
        ):
            job_instance.tuesday
        with self.assertRaisesRegex(
            IntervalError, (
                        r'Scheduling \.wednesday\(\) job is only allowed for weekly jobs\.'
                        r'Using \.wednesday\(\) on a job scheduled to tun every 2 or more weeks'
                        r'is ont supported'
                )
        ):
            job_instance.wednesday
        with self.assertRaisesRegex(
            IntervalError, (
                        r'Scheduling \.thursday\(\) job is only allowed for weekly jobs\.'
                        r'Using \.thursday\(\) on a job scheduled to tun every 2 or more weeks'
                        r'is ont supported'
                )
        ):
            job_instance.thursday
        with self.assertRaisesRegex(
            IntervalError, (
                        r'Scheduling \.friday\(\) job is only allowed for weekly jobs\.'
                        r'Using \.friday\(\) on a job scheduled to tun every 2 or more weeks'
                        r'is ont supported'
                )
        ):
            job_instance.friday

        job_instance.unit = 'FOO'
        self.assertRaises(SchedulerValueError, job_instance.at, '1:0:0')
        self.assertRaises(SchedulerValueError, job_instance._scheduler_next_run)

        job_instance.unit = 'days'
        job_instance.start_day = 1
        self.assertRaises(SchedulerValueError, job_instance._scheduler_next_run)

        job_instance.unit = 'weeks'
        job_instance.start_day = 'bre'
        self.assertRaises(SchedulerValueError, job_instance._scheduler_next_run)

        job_instance.unit = 'deys'
        self.assertRaises(SchedulerValueError, job_instance.at, '25:00:00')
        self.assertRaises(SchedulerValueError, job_instance.at, '00:61:00')
        self.assertRaises(SchedulerValueError, job_instance.at, '00:00:61')
        self.assertRaises(SchedulerValueError, job_instance.at, '25:0:0')
        self.assertRaises(SchedulerValueError, job_instance.at, '0:61:0')
        self.assertRaises(SchedulerValueError, job_instance.at, '0:0:61')

        job_instance.unit = 'seconds'
        job_instance.at_time = datetime.now()
        job_instance.start_day = None
        self.assertRaises(SchedulerValueError, job_instance._scheduler_next_run)

        job_instance.latest = 1
        self.assertRaises(SchedulerError, job_instance._scheduler_next_run)

    def test_next_run_with_tag(self):
        with mock_datetime(2014, 6, 28, 12, 0):
            job1 = every(5).seconds.do(make_mock_job(name='job1')).tag('tag1')
            job2 = every(2).seconds.do(make_mock_job(name='job2')).tag('tag1', 'tag2')
            job3 = every(1).seconds.do(make_mock_job(name='job3')).tag('tag1', 'tag2', 'tage3')
            assert scheduler.get_next_run('tag1') == job1.next_run
            assert scheduler.default_scheduler.get_next_run('tage2') == job3.next_run
            assert scheduler.get_next_run('tag3') == job3.next_run
            assert scheduler.get_next_run('tage4') is None

    def test_singular_time_units_match_plural_units(self):
        assert every().second.unit == every().seconds.unit
        assert every().minute.unit == every().minutes.unit
        assert every().hour.unit == every().hours.unit
        assert every().day.unit == every().days.unit
        assert every().week.unit == every().weeks.unit
