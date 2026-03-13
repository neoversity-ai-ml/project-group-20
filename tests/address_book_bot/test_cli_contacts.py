from textwrap import dedent

from helpers import (
    run_cli,
    mock_data_io,
    assert_mock_called_n_times_with,
    formatted_output,
)

from address_book_bot.models import AddressBook


def test_contacts_management(capsys, monkeypatch):
    book = AddressBook()

    commands_to_response = (
        ("add John 1234567890", "Contact added."),
        ("add Jane 3987654321", "Contact added."),
        ("change John 1234567890 2987654321", "Contact changed."),
        ("phone John", "2987654321"),
        ("add-birthday John 01.01.1990", "Birthday added."),
        ("show-birthday John", "01.01.1990"),
        (
            "birthdays",
            "Please provide the number of days to check for upcoming birthdays.",
        ),
        ("add-address John 123 Main St", "Address added."),
        ("add-email John john@example.com", "Email added."),
        ("show-email John", "john@example.com"),
        ("change-email John john.doe@example.com", "Email added."),
        ("change-address John 456 Elm St", "Address added."),
        ("delete-phone John 2987654321", "Phone 2987654321 removed."),
        ("phone John", "No phone numbers found for this contact."),
        (
            "all",
            dedent("""\
                Contact name: John, phones: -, birthday: 01.01.1990, address: 456 Elm St, email: john.doe@example.com
                Contact name: Jane, phones: 3987654321"""),
        ),
        ("search Jane", "Contact name: Jane, phones: 3987654321"),
        ("search 3987654321", "Contact name: Jane, phones: 3987654321"),
        (
            "search Elm",
            "Contact name: John, phones: -, birthday: 01.01.1990, address: 456 Elm St, email: john.doe@example.com",
        ),
        (
            "search john.doe@example.com",
            "Contact name: John, phones: -, birthday: 01.01.1990, address: 456 Elm St, email: john.doe@example.com",
        ),
        ("delete-address John", "Address removed."),
        ("delete-email John", "Email removed."),
        ("show-email John", "Email not set for this contact."),
        ("exit", "Good bye!"),
    )

    with mock_data_io(book) as (mock_save, mock_load):
        commands = [command for command, _ in commands_to_response]
        expected = formatted_output(commands_to_response)

        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands) - 1, (book,))
