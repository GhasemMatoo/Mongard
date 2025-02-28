import pytest
import time
from person import Person


class TestPerson:
    @pytest.fixture
    def setup(self):
        self.p1 = Person("john", 'vatson')
        self.p2 = Person("jak", "danyels")
        yield 'setup'
        time.sleep(2)

    def test_full_name(self, setup):
        assert self.p1.full_name() == 'john vatson'
        assert self.p2.full_name() == 'jak danyels'
        assert isinstance(self.p1, Person)
        with pytest.raises(AttributeError):
            assert isinstance(self.p3, Person)

    def test_email(self, setup):
        assert self.p1.email() == 'john.vatson@email.com'
        assert self.p2.email() == 'jak.danyels@email.com'
