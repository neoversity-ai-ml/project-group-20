from datetime import date

from tests.cli.helpers import (
    run_cli,
    mock_data_io,
    assert_mock_called_n_times_with,
    formatted_output,
)

from models import AddressBook


def test_error_handling(capsys, monkeypatch):
    book = AddressBook()
    bob_bday = date.today()

    commands_to_response = (
        ("change-phone Jane 1234567890 1234567890", "Contact not found."),
        ("show-phone", "Please provide only name to show the phone."),
        ("add-birthday John 01.01.1990", "Contact not found."),
        ("add-birthday John", "Please provide only contact name and birthday."),
        ("show-birthday Jane", "Contact not found."),
        ("add-address John 123 Main St", "Contact not found."),
        ("add-email John johnexample.com", "Contact not found."),
        ("show-email", "Please provide only contact name."),
        ("change-email Jane", "Please provide name and email."),
        ("change-address John", "Please provide name and address: name address."),
        ("change-address Jane", "Please provide name and address: name address."),
        ("delete-phone Jane 1234567890", "Contact not found."),
        ("show-phone Jane", "Contact not found."),
        ("delete-email Jane", "Contact not found."),
        ("show-email Jane", "Contact not found."),
        ("delete-address Jane", "Contact not found."),
        ("all", "No contacts found."),
        ("birthdays 7", "No upcoming birthdays during requested period."),
        (
            "birthdays -1",
            "Please provide the number of days to check for upcoming birthdays.",
        ),
        ("birthdays 366", "Days must be a positive number and not exceed 365."),
        ("add Bob 1234567890", "Contact added."),
        ("show-birthday Bob", "Birthday not set for this contact."),
        (f"add-birthday Bob {bob_bday.strftime('%d.%m.%Y')}", "Birthday added."),
        (
            "birthdays 7",
            f"{bob_bday.strftime('%d.%m.%Y')} Bob ({bob_bday.strftime('%A')})",
        ),
        ("search Jane", "No contacts found."),
        ("add-email Bob bobexample.com", "Invalid email address format."),
        ("add Jane 1111111111", "Phone number cannot consist of all identical digits."),
        ("add Jane 0111111111", "Phone number cannot start with 0."),
        ("delete-phone Bob 1234567891", "Phone number not found."),
        (
            "change-phone Bob 1234567891",
            "Please provide only contact name and existing/new phone numbers.",
        ),
        ("change-phone Bob 1234567891 1234567891", "Phone number to edit not found."),
        ("delete-address Bob", "Address not found."),
        ("delete-email Bob", "Email not found."),
        ("show-birthday", "Please provide only name to show the birthday."),
        ("search", "Please provide some query to search for."),
        ("delete-address", "Please provide only contact name."),
        ("delete-email", "Please provide only contact name."),
        ("delete-email Jane 123", "Please provide only contact name."),
        ("add", "Please provide only contact name and phone number."),
        ("delete-phone", "Please provide only contact name and phone number."),
        ("exit", "Good bye!"),
    )

    with mock_data_io(book) as (mock_save, mock_load):
        commands = [command for command, _ in commands_to_response]
        expected = formatted_output(commands_to_response)

        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands) - 1, (book,))
