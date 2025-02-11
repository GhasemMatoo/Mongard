from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from home.forms import UserRegistrationForm
from home.views import WriterView


class TestUserRegisterViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse('home:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, WriterView.template_name)
        self.assertTrue(response.context['form'], UserRegistrationForm)

    def test_user_register_POST_valid(self):
        response = self.client.post(
            reverse('home:user_register'),
            data={
                'user_name': 'ghasem',
                'user_email': 'matoogsm90@gmail.com',
                'user_password': 'matoo',
                'user_re_password': 'matoo',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home:home"))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        response = self.client.post(
            reverse('home:user_register'),
            data={
                'user_name': 'ghasem',
                'user_email': 'matoogsm90@gma',
                'user_password': 'matoo',
                'user_re_password': 'matoo',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())

