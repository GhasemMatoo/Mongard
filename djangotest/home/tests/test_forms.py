from django.test import TestCase
from home.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestUserRegistrationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='ghasems',
            email='matoogsm900@gmail.com',
            password='Mg136868',
        )

    def test_validat_data(self):
        form = UserRegistrationForm(
            data={
                'user_name': "ghasem",
                'user_email': "matoogsm90@gmail.com",
                'user_password': 123456,
                'user_re_password': 123456
            }
        )
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exist_email(self):

        form = UserRegistrationForm(
            data={
                'user_name': 'not_matoo',
                'user_email': 'matoogsm900@gmail.com',
                'user_password': 'Mg136868',
                'user_re_password': 'Mg136868',
            }
        )
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)
