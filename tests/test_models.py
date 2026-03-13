import pytest
from datetime import date

from address_book_bot.models import AddressBook, Record


@pytest.fixture
def address_book():
    book = AddressBook()
    book.add_record(Record("John Doe"))
    return book


def test_delete_existing_contact(address_book):
    address_book.delete("John Doe")
    assert "John Doe" not in address_book.data


def test_delete_non_existing_contact_raises_key_error(address_book):
    with pytest.raises(KeyError):
        address_book.delete("Jane Doe")


def test_get_upcoming_birthdays():
    book = AddressBook()

    record1 = Record("Bill")
    record1.add_birthday("26.12.1990")
    book.add_record(record1)

    record2 = Record("Jill")
    record2.add_birthday("28.12.1985")
    book.add_record(record2)

    record3 = Record("Kim")
    record3.add_birthday("29.12.1995")
    book.add_record(record3)

    record4 = Record("Tom")
    record4.add_birthday("01.01.2000")
    book.add_record(record4)

    record5 = Record("Kate")
    record5.add_birthday("15.01.1992")
    book.add_record(record5)

    book.add_record(Record("Blank"))

    upcoming = book.get_upcoming_birthdays(10, today=date(2024, 12, 23))

    assert len(upcoming) == 4

    expected_dates = {
        "Bill": date(2024, 12, 26),
        "Jill": date(2024, 12, 30),
        "Kim": date(2024, 12, 30),
        "Tom": date(2025, 1, 1),
    }

    for person in upcoming:
        assert person["name"] in expected_dates
        assert person["congratulation_date"] == expected_dates[person["name"]]

    assert upcoming[0]["name"] == "Bill"
    assert upcoming[3]["name"] == "Tom"
    assert {upcoming[1]["name"], upcoming[2]["name"]} == {"Jill", "Kim"}


def test_get_upcoming_birthdays_no_results():
    book = AddressBook()
    record = Record("Far Bday")
    record.add_birthday("10.10.1990")
    book.add_record(record)

    upcoming = book.get_upcoming_birthdays(7, today=date(2024, 5, 20))
    assert upcoming == []
