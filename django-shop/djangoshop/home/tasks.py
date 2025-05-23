from bucket import bucket
from celery import shared_task


def all_bucket_objects_task():
    return bucket.get_object()


@shared_task
def delete_object_task(key):
    bucket.delete_object(key=key)


@shared_task
def download_object_task(key):
    bucket.download_object(key=key)
