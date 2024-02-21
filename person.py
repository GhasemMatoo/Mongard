class Person:
    def __init__(self, forename, surname):
        self.forename = forename
        self.surname = surname

    def full_name(self):
        return f"{self.forename} {self.surname}"

    def email(self):
        return f"{self.full_name()}@email.com".replace(' ', '.')

