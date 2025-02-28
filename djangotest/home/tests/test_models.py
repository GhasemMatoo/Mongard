from django.test import TestCase
from home.models import Writer
from model_bakery import baker


class TestWriter(TestCase):
    def setUp(self):
        # self.writer = Writer.objects.create(
        #     first_name="ghasem",
        #     last_name="Matoo",
        #     email='matoogsm90@gmai',
        #     country="iran"
        # )
        self.writer = baker.make(Writer, first_name="ghasem", last_name="Matoo",)

    def test_model_str(self):
        self.assertEqual(self.writer.__str__(), "ghasem Matoo")
