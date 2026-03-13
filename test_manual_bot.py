from main import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_address,
)
from models import AddressBook
from datetime import datetime, timedelta

if __name__ == "__main__":  # pragma: no cover
    book = AddressBook()

    print(add_contact(["John", "+1234567890"], book))
    print(add_contact(["John", "+5555555555"], book))
    print(show_phone(["John"], book))
    print(add_contact(["Jack", "+(23)9876543210"], book))
    print(add_contact(["Bob", "5551234567"], book))
    print(add_contact(["Bobs", "5551214567"], book))

    print(change_contact(["John", "1234567890", "1112223333"], book))
    print(show_phone(["John"], book))

    print(
        add_birthday(
            ["John", (datetime.today() + timedelta(days=2)).strftime("%d.%m.%Y")], book
        )
    )
    print(show_birthday(["John"], book))
    print(
        add_birthday(
            ["Jack", (datetime.today() + timedelta(days=15)).strftime("%d.%m.%Y")], book
        )
    )
    print(
        add_birthday(
            ["Bob", (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y")], book
        )
    )
    print(
        add_birthday(
            ["Bobs", (datetime.today() + timedelta(days=3)).strftime("%d.%m.%Y")], book
        )
    )

    # valid cases
    print(add_address(["John", "Main St, Kyiv, 01001, Ukraine"], book))
    print(add_address(["Bob", "Baker St, London, NW1 6XE, UK"], book))

    # contact not found
    print(add_address(["Unknown", "Some St, City, 00000, Country"], book))

    # too few arguments (only name, no address)
    print(add_address(["John"], book))

    # no arguments at all
    print(add_address([], book))

    # print(show_all(book))
    print(birthdays(["10"], book))
