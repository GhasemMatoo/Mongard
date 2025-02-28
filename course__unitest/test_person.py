from unittest import TestCase
from person import Person


class PersonTest(TestCase):
    def setUp(self):
        self.p1 = Person("john", 'vatson')
        self.p2 = Person("jak", "danyels")

    def tearDown(self):
        print("Done")

    def test_full_name(self):
        self.assertEquals(self.p1.full_name(), 'john vatson')
        self.assertEquals(self.p2.full_name(), 'jak danyels')
        self.assertIsInstance(self.p1, Person)

    def test_email(self):
        self.assertEquals(self.p1.email(), 'john.vatson@email.com')
        self.assertEquals(self.p2.email(), 'jak.danyels@email.com')
