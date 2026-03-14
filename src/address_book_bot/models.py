import re
from collections import Counter, UserDict
from datetime import date, datetime, timedelta

from .constant import STOP_WORDS, WORD_PATTERN


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
    ValueError: Phone number must be 7-15 digits, optionally with +, spaces, dashes, or parentheses.
    >>> Phone("12345")
    Traceback (most recent call last):
        ...
    ValueError: Phone number must be 7-15 digits, optionally with +, spaces, dashes, or parentheses.
    """

    def __init__(self, value):
        if not re.fullmatch(r"^\+?[\d\s\-\(\)]{7,15}$", value):
            raise ValueError("Phone number must be 7-15 digits, optionally with +, spaces, dashes, or parentheses.")
        digits = re.sub(r"[\s\-\(\)]", "", value).lstrip("+")
        if len(set(digits)) == 1:
            raise ValueError("Phone number cannot consist of all identical digits.")
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
    datetime.date(1990, 12, 25)
    >>> Birthday("32.12.1990")
    Traceback (most recent call last):
        ...
    ValueError: Invalid date format. Use DD.MM.YYYY
    """

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError as err:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from err

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Note(Field):
    """Class for storing a text note."""

    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Note cannot be empty.")
        super().__init__(value)
        self._word_counts = self._calculate_word_counts(value)
        self.tags = [word for word, count in self._word_counts.most_common(3)]

    def _calculate_word_counts(self, text):
        words = WORD_PATTERN.findall(text.lower())
        filtered_words = [word for word in words if word not in STOP_WORDS]
        return Counter(filtered_words)

    def get_tag_count(self, tag):
        return self._word_counts.get(tag.lower(), 0)

    def __repr__(self):
        tags_str = ", ".join(self.tags)
        return f"Note('{self.value}') [Tags: {tags_str}]"


class Address(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    """Class for storing contact information."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
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

    def add_address(self, address):
        self.address = Address(address)

    def remove_address(self):
        if self.address:
            self.address = None
        else:
            raise ValueError("Address not found.")

    def add_email(self, email):
        self.email = Email(email)

    def remove_email(self):
        if self.email:
            self.email = None
        else:
            raise ValueError("Email not found.")

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "-"
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        address_str = f", address: {self.address}" if self.address else ""
        email_str = f", email: {self.email}" if self.email else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}{address_str}{email_str}"


class AddressBook(UserDict):
    """Class for managing an address book of contacts."""

    def __init__(self):
        super().__init__()
        self.notes = []

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError

    def get_upcoming_birthdays(self, days, today=None):
        """Returns contacts with birthdays in the upcoming requested period, sorted by date."""

        upcoming = []
        today = today or date.today()

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                if 0 <= delta_days < days:
                    congratulation_date = birthday_this_year
                    if congratulation_date.strftime("%A") in ["Saturday", "Sunday"]:
                        days_until_monday = (7 - congratulation_date.weekday()) % 7
                        congratulation_date = congratulation_date + timedelta(days=days_until_monday)
                    upcoming.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": congratulation_date,
                        }
                    )
        return sorted(upcoming, key=lambda x: x["congratulation_date"])

    def add_note(self, text):
        note = Note(text)
        self.notes.append(note)
        return f"Note added with tags: {', '.join(note.tags)}"

    def edit_note(self, index, new_text):
        if index < 0 or index >= len(self.notes):
            raise ValueError("Invalid note number.")
        self.notes[index] = Note(new_text)

    def delete_note(self, index):
        if index < 0 or index >= len(self.notes):
            raise ValueError("Invalid note number.")
        del self.notes[index]

    def search_notes(self, keyword):
        keyword = keyword.strip().lower()
        if not keyword:
            raise ValueError("Search keyword cannot be empty.")

        return [note for note in self.notes if keyword in note.value.lower()]

    def search_notes_by_tag(self, tag):
        tag = tag.strip().lower()
        filtered = [note for note in self.notes if tag in note.tags]
        filtered.sort(key=lambda n: (-n.get_tag_count(tag), n.value.lower()))
        return filtered

    def sort_notes_by_tags(self):
        self.notes.sort(
            key=lambda note: (
                len(note.tags) == 0,
                note.tags[0].lower() if note.tags else "",
                -note.get_tag_count(note.tags[0]) if note.tags else 0,
            )
        )
        return self.notes

    def search(self, query):
        query = query.lower()
        results = []

        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
                continue

            found_in_phones = any(query in phone.value for phone in record.phones)
            if found_in_phones:
                results.append(record)
                continue

            if record.email and query in record.email.value.lower():
                results.append(record)
                continue

            if record.address and query in record.address.value.lower():
                results.append(record)
                continue

            if record.birthday and query in str(record.birthday).lower():
                results.append(record)
                continue

        for note in self.notes:
            in_note_text = query in note.value.lower()
            in_tags = any(query in tag.lower() for tag in note.tags)

            if in_note_text or in_tags:
                results.append(note)

        return results
