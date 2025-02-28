from django.test import TestCase
from django.urls import resolve, reverse
from home.views import Home, About


class TestUrls(TestCase):

    def test_home(self):
        url = reverse('home:home')  # urls path "/"
        self.assertEqual(resolve(url).func.view_class, Home)

    def test_about(self):
        url = reverse('home:about', kwargs={"username": "matoo"})
        self.assertEqual(resolve(url).func.view_class, About)

