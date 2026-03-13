import textwrap

from helpers import run_cli, mock_data_io, assert_mock_called_n_times_with

from address_book_bot.models import AddressBook


def test_contacts_management(capsys, monkeypatch):
    book = AddressBook()

    commands = (
        "add John 1234567890",
        "add Jane 3987654321",
        "change-phone John 1234567890 2987654321",
        "show-phone John",
        "add-birthday John 01.01.1990",
        "show-birthday John",
        "birthdays",
        "add-address John 123 Main St",
        "add-email John john@example.com",
        "show-email John",
        "change-email John john.doe@example.com",
        "change-address John 456 Elm St",
        "delete-phone John 2987654321",
        "show-phone John",
        "all",
        "search Jane",
        "search 3987654321",
        "search Elm",
        "search john.doe@example.com",
        "delete-address John",
        "delete-email John",
        "show-email John",
        "exit",
    )

    expected = textwrap.dedent("""\
        Welcome to the assistant bot!
        Contact added.
        Contact added.
        Contact changed.
        2987654321
        Birthday added.
        01.01.1990
        Please provide the number of days to check for upcoming birthdays.
        Address added.
        Email added.
        john@example.com
        Email added.
        Address added.
        Phone 2987654321 removed.
        No phone numbers found for this contact.
        Contact name: John, phones: -, birthday: 01.01.1990, address: 456 Elm St, email: john.doe@example.com
        Contact name: Jane, phones: 3987654321
        Contact name: Jane, phones: 3987654321
        Contact name: Jane, phones: 3987654321
        Contact name: John, phones: -, birthday: 01.01.1990, address: 456 Elm St, email: john.doe@example.com
        Contact name: John, phones: -, birthday: 01.01.1990, address: 456 Elm St, email: john.doe@example.com
        Address removed.
        Email removed.
        Email not set for this contact.
        Good bye!
    """)

    with mock_data_io(book) as (mock_save, mock_load):
        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands) - 1, (book,))
