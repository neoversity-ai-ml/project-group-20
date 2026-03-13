from helpers import (
    run_cli,
    mock_data_io,
    assert_mock_called_n_times_with,
    formatted_output,
)

from address_book_bot.models import AddressBook


def test_hello(capsys, monkeypatch):
    book = AddressBook()

    commands_to_response = (
        ("hello", "How can I help you?"),
        (" ", None),
        ("", None),
        ("all", "No contacts found."),
        ("as,dmna,sd", "Invalid command."),
        ("exit", "Good bye!"),
    )

    with mock_data_io(book) as (mock_save, mock_load):
        commands = [command for command, _ in commands_to_response]
        expected = formatted_output(commands_to_response)

        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands) - 3, (book,))
