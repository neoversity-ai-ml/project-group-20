from datetime import date
import textwrap

from tests.cli.helpers import run_cli, mock_data_io, assert_mock_called_n_times_with

from models import AddressBook


def test_contacts_management(capsys, monkeypatch):
    book = AddressBook()
    bob_bday = date.today()

    commands = (
        "change-phone Jane 1234567890 1234567890",
        "show-phone",
        "add-birthday John 01.01.1990",
        "show-birthday Jane",
        "add-address John 123 Main St",
        "add-email John johnexample.com",
        "show-email",
        "change-email Jane",
        "change-address John",
        "change-address Jane",
        "delete-phone Jane 1234567890",
        "show-phone Jane",
        "delete-email Jane",
        "show-email Jane",
        "delete-address Jane",
        "all",
        "birthdays 7",
        "birthdays -1",
        "birthdays 366",
        "add Bob 1234567890",
        "show-birthday Bob",
        f"add-birthday Bob {bob_bday.strftime('%d.%m.%Y')}",
        "birthdays 7",
        "search Jane",
        "add-email Bob bobexample.com",
        "add Jane 1111111111",
        "add Jane 0111111111",
        "delete-phone Bob 1234567891",
        "change-phone Bob 1234567891 1234567891",
        "delete-address Bob",
        "delete-email Bob",
        "exit",
    )

    expected = textwrap.dedent(f"""\
        Welcome to the assistant bot!
        Contact not found.
        not enough values to unpack (expected 1, got 0)
        Contact not found.
        Contact not found.
        Contact not found.
        Contact not found.
        not enough values to unpack (expected 1, got 0)
        not enough values to unpack (expected 2, got 1)
        Please provide name and address: name address.
        Please provide name and address: name address.
        Contact not found.
        Contact not found.
        Contact not found.
        Contact not found.
        Contact not found.
        No contacts found.
        No upcoming birthdays during requested period.
        Please provide the number of days to check for upcoming birthdays.
        Days must be a positive number and not exceed 365.
        Contact added.
        Birthday not set for this contact.
        Birthday added.
        {bob_bday.strftime("%d.%m.%Y")} Bob ({bob_bday.strftime("%A")})
        No contacts found.
        Invalid email address format.
        Phone number cannot consist of all identical digits.
        Phone number cannot start with 0.
        Phone number not found.
        Phone number to edit not found.
        Address not found.
        Email not found.
        Good bye!
    """)

    with mock_data_io(book) as (mock_save, mock_load):
        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands), (book,))
