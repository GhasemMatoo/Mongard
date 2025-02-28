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

    def test_log_ip_remote(self):
        remote_addr = '127.0.0.9'
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, remote_addr)

    def test_log_ip_remote_list(self):
        remote_addr = '127.0.0.9, 128.1.1.9'
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "127.0.0.9")

    def test_log_ip_remote_v4_with_port(self):
        remote_addr = '127.0.0.9:1234'
        re_remote_addr = '127.0.0.9'
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, re_remote_addr)

    def test_log_ip_remote_v6(self):
        remote_addr = '2001:db8:85a3:0000:0000:2001:8db8:85a3'
        re_remote_addr = '2001:db8:85a3::2001:8db8:85a3'
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, re_remote_addr)

    def test_log_ip_remote_v6_loopback(self):
        remote_addr = '::1'
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, remote_addr)

    def test_log_ip_remote_v6_with_port(self):
        remote_addr = '[::1]:1234'
        re_remote_addr = '::1'
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, re_remote_addr)

    def test_log_ip_x_forwarded(self):
        remote_addr = '127.0.08'
        request = APIRequestFactory().get('/logging/')
        request.META['HTTP_X_FORWARDED_FOR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, remote_addr)

    def test_log_ip_x_forwarded_list(self):
        remote_addr = '127.0.08, 128.1.1.9'
        re_remote_addr = '127.0.08'
        request = APIRequestFactory().get('/logging/')
        request.META['HTTP_X_FORWARDED_FOR'] = remote_addr
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, re_remote_addr)

    def test_log_host(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.host, 'testserver')

    def test_log_method(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.method, 'GET')

    def test_log_status(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.status_code, 200)
