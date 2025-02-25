from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from tracking.models import APIRequestLog
from django.test import override_settings
from .views import MockLoggingView


@override_settings(ROOT_URLCONF='tracking.tests.urls')
class TestLoggingMixin(APITestCase):
    def test_nologging_no_log_created(self):
        self.client.get("/no-logging/")
        # self.client.get(reverse("tracking:test:no-logging"))
        self.assertEqual(APIRequestLog.objects.all().count(), 0)

    def test_logging_creates_lod(self):
        self.client.get("/logging/")
        self.assertEqual(APIRequestLog.objects.all().count(), 1)

    def test_log_path(self):
        url = "/logging/"
        self.client.get(url)
        log = APIRequestLog.objects.first()
        self.assertEqual(log.path, url)
