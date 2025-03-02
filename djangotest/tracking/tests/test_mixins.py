import ast
import datetime

from rest_framework.test import APITestCase, APIRequestFactory
from tracking.models import APIRequestLog
from django.test import override_settings
from django.contrib.auth.models import User
from unittest import mock
from .views import MockLoggingView
from tracking.mixins import BaseLoggingMixin


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

    def test_logging_explicit(self):
        url = '/explicit-logging/'
        self.client.get(url)
        self.client.post(url)
        self.assertEqual(APIRequestLog.objects.all().count(), 1)

    def test_custom_check_logging(self):
        url = "/custom-check-logging/"
        self.client.get(url)
        self.client.post(url)
        self.assertEqual(APIRequestLog.objects.all().count(), 1)

    def test_log_anon_user(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.user, None)

    def test_log_auth_user(self):
        username = 'ghasem'
        password = '1234'
        User.objects.create_user(username=username, password=password)
        user = User.objects.get(username=username)

        self.client.login(username=username, password=password)
        self.client.get('/session-auth-logging/')

        log = APIRequestLog.objects.first()
        self.assertEqual(log.user, user)

    def test_log_params(self):
        self.client.get('/logging/', {'p1': 'a', 'another': '2'})
        log = APIRequestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params), {'p1': 'a', 'another': '2'})

    def test_log_params_cleaned_form_personal_list(self):
        params = {'api': "123456", 'capitalized': "123456", 'my_field': "123456"}
        self.client.get('/sensitive-fields-logging/', params)
        log = APIRequestLog.objects.first()
        self.assertEqual(
            ast.literal_eval(log.query_params),
            {
                'api': BaseLoggingMixin.CLEANED_SUBSTITUTE,
                'capitalized': "123456",
                'my_field': BaseLoggingMixin.CLEANED_SUBSTITUTE
            }
        )

    def test_invalid_cleaned_substitute_fails(self):
        with self.assertRaises(AssertionError):
            self.client.get('/invalid-cleaned-substitute-logging/')

    @mock.patch('tracking.models.APIRequestLog.save')
    def test_log_doesnt_prevent_api_call_if_log_save_fails(self, mocked_save):
        mocked_save.side_effect = Exception('db failure')
        response = self.client.get('/logging/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(APIRequestLog.objects.all().count(), 0)

    @mock.patch('tracking.base_mixins.now')
    def test_log_doesnt_fail_whit_negative_response_ms(self, mocked_now):
        mocked_now.side_effect = [
            datetime.datetime(2020, 12, 1, 0, 10),
            datetime.datetime(2020, 12, 1, 0, 0)
        ]
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.response_ms, 0)
