from celery import shared_task
from accounts.models import OtpCode
from datetime import datetime, timedelta
from pytz import timezone


@shared_task
def remove_expired_oto_codes():
    expired_time = datetime.now(tz=timezone('Asia/Tehran')) - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()
