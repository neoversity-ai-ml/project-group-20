import textwrap

from helpers import run_cli, mock_data_io, assert_mock_called_n_times_with

from address_book_bot.models import AddressBook


def test_hello(capsys, monkeypatch):
    book = AddressBook()

    commands = (
        "hello",
        " ",
        "",
        "all",
        "as,dmna,sd",
        "exit",
    )

    expected = textwrap.dedent("""\
        Welcome to the assistant bot!
        How can I help you?
        No contacts found.
        Invalid command.
        Good bye!
    """)

    with mock_data_io(book) as (mock_save, mock_load):
        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands) - 3, (book,))
