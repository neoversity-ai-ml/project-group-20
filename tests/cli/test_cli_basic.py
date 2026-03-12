import textwrap

from tests.cli.helpers import run_cli, mock_data_io

from models import AddressBook


def test_hello(capsys, monkeypatch):
    book = AddressBook()

    commands = (
        "hello",
        "all",
        "exit",
    )

    expected = textwrap.dedent("""\
        Welcome to the assistant bot!
        How can I help you?
        No contacts found.
        Good bye!
    """)

    with mock_data_io(book) as (mock_save, mock_load):
        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        mock_save.assert_called_once_with(book)
