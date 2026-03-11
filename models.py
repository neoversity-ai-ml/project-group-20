import re
from collections import UserDict, defaultdict
from datetime import date, datetime


class Field:
    """Base class for record fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing a contact's name."""

    pass


class Phone(Field):
    """
    Class for storing and validating a phone number.

    >>> Phone("1234567890")
    Phone('1234567890')
    >>> Phone("invalid-phone")
    Traceback (most recent call last):
        ...
    ValueError: Phone number must be 10 digits.
    >>> Phone("12345")
    Traceback (most recent call last):
        ...
    ValueError: Phone number must be 10 digits.
    """

    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    def __repr__(self):
        return f"Phone('{self.value}')"

class Email(Field):
    def __init__(self, value):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address format.")
        super().__init__(value)

class Birthday(Field):
    """
    Class for storing and validating a birthday.

    >>> b = Birthday("25.12.1990")
    >>> b.value
    datetime.datetime(1990, 12, 25, 0, 0)
    >>> Birthday("32.12.1990")
    Traceback (most recent call last):
        ...
    ValueError: Invalid date format. Use DD.MM.YYYY
    """

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Class for storing contact information."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone_number, new_phone_number):
        phone_to_edit = self.find_phone(old_phone_number)
        if phone_to_edit:
            phone_to_edit.value = Phone(new_phone_number).value
        else:
            raise ValueError("Phone number to edit not found.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}{email_str}"


class AddressBook(UserDict):
    """Class for managing an address book of contacts."""

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError

    def get_upcoming_birthdays(self):
        """Returns contacts with birthdays in the upcoming week, grouped by day."""

        birthdays_by_day = defaultdict(list)
        today = date.today()

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.date().replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                if 0 <= delta_days < 7:
                    day_of_week = birthday_this_year.strftime('%A')
                    if day_of_week in ['Saturday', 'Sunday']:
                        day_of_week = 'Monday'
                    birthdays_by_day[day_of_week].append(record.name.value)
        return birthdays_by_day


if __name__ == "__main__":
    import doctest
    doctest.testmod()
