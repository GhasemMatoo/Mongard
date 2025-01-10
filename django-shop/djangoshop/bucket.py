import boto3
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io


class Bucket:
    """
    CDN Buket manager
    init methode creates connection.
    """

    def __init__(self):
        session = boto3.session.Session()
        self.config = boto3.client(
            service_name=settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def get_object(self):
        result = self.config.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if len(result['Contents']) > 0:
            return result['Contents']
        return None

    def delete_object(self, key):
        self.config.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.config.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)

    def upload_object(self, file):
        path = default_storage.save(file.name, ContentFile(file.read()))
        return True


bucket = Bucket()
