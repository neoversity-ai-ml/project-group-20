from main import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)
from models import AddressBook
from datetime import datetime, timedelta

book = AddressBook()

print(add_contact(["John", "1234567890"], book))
print(add_contact(["John", "5555555555"], book))
print(show_phone(["John"], book))
print(add_contact(["Jack", "9876543210"], book))
print(add_contact(["Bob", "5551234567"], book))

print(change_contact(["John", "1234567890", "1112223333"], book))
print(show_phone(["John"], book))

print(add_birthday(["John", (datetime.today() + timedelta(days=2)).strftime("%d.%m.%Y")], book))
print(show_birthday(["John"], book))
print(add_birthday(["Jack", (datetime.today() + timedelta(days=15)).strftime("%d.%m.%Y")], book))
print(add_birthday(["Bob", (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y")], book))

print(show_all(book))
print(birthdays("10", book))