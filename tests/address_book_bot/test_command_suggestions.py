from textwrap import dedent

from helpers import (
    run_cli,
    mock_data_io,
    assert_mock_called_n_times_with,
    formatted_output,
)

from address_book_bot.models import AddressBook


def test_regexp_resolved_commands(capsys, monkeypatch):
    book = AddressBook()

    commands_to_response = (
        (
            "hi",
            dedent("""\
            Command not found. Did you mean:
              hello"""),
        ),
        (
            "Hey",
            dedent("""\
            Command not found. Did you mean:
              hello"""),
        ),
        (
            "привіт",
            dedent("""\
            Command not found. Did you mean:
              hello"""),
        ),
        (
            "heyy",
            dedent("""\
            Command not found. Did you mean:
              hello"""),
        ),
        (
            "quit",
            dedent("""\
            Command not found. Did you mean:
              exit
              close"""),
        ),
        (
            "break",
            dedent("""\
            Command not found. Did you mean:
              exit
              close"""),
        ),
        (
            "quitt",
            dedent("""\
            Command not found. Did you mean:
              exit
              close"""),
        ),
        (
            "insert",
            dedent("""\
            Command not found. Did you mean:
              add Name 1234567890
              add-birthday Name 01.01.1990"""),
        ),
        (
            "create",
            dedent("""\
            Command not found. Did you mean:
              add Name 1234567890
              add-birthday Name 01.01.1990"""),
        ),
        (
            "Insert ",
            dedent("""\
            Command not found. Did you mean:
              add Name 1234567890
              add-birthday Name 01.01.1990"""),
        ),
        (
            "edit",
            dedent("""\
            Command not found. Did you mean:
              change Name 1234567890 1234567891
              add-birthday Name 01.01.1990"""),
        ),
        (
            "modify",
            dedent("""\
            Command not found. Did you mean:
              change Name 1234567890 1234567891
              add-birthday Name 01.01.1990"""),
        ),
        (
            "eDit  ",
            dedent("""\
            Command not found. Did you mean:
              change Name 1234567890 1234567891
              add-birthday Name 01.01.1990"""),
        ),
        (
            "del",
            dedent("""\
            Command not found. Did you mean:
              delete contact
              delete birthday"""),
        ),
        (
            "delete",
            dedent("""\
            Command not found. Did you mean:
              delete contact
              delete birthday"""),
        ),
        (
            "remove",
            dedent("""\
            Command not found. Did you mean:
              delete contact
              delete birthday"""),
        ),
        (
            " del  ",
            dedent("""\
            Command not found. Did you mean:
              delete contact
              delete birthday"""),
        ),
        (
            "show",
            dedent("""\
            Command not found. Did you mean:
              all
              birthdays
              show-birthday Name
              phone Name"""),
        ),
        (
            "display",
            dedent("""\
            Command not found. Did you mean:
              all
              birthdays
              show-birthday Name
              phone Name"""),
        ),
        (
            "list",
            dedent("""\
            Command not found. Did you mean:
              all
              birthdays
              show-birthday Name
              phone Name"""),
        ),
        (
            "birth",
            dedent("""\
            Command not found. Did you mean:
              birthdays
              add-birthday Name 01.01.1990
              show-birthday Name"""),
        ),
        (
            "day",
            dedent("""\
            Command not found. Did you mean:
              birthdays
              add-birthday Name 01.01.1990
              show-birthday Name"""),
        ),
        (
            "find",
            dedent("""\
            Command not found. Did you mean:
              phone Name
              change Name 1234567890 1234567891"""),
        ),
        (
            "call",
            dedent("""\
            Command not found. Did you mean:
              phone Name
              change Name 1234567890 1234567891"""),
        ),
        (
            "number",
            dedent("""\
            Command not found. Did you mean:
              phone Name
              change Name 1234567890 1234567891"""),
        ),
    )

    with mock_data_io(book) as (mock_save, mock_load):
        commands = [command for command, _ in commands_to_response]
        expected = formatted_output(commands_to_response)

        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands), (book,))


def test_fuzzy_resolved_commands(capsys, monkeypatch):
    book = AddressBook()

    commands_to_response = (
        (
            "helloo",
            dedent("""\
            Command not found. Did you mean:
              hello"""),
        ),
        (
            "HE LLO",
            dedent("""\
            Command not found. Did you mean:
              phone LLO
              hello LLO
              change LLO"""),
        ),
        (
            "exittt",
            dedent("""\
            Command not found. Did you mean:
              exit
              edit-note 1 new text"""),
        ),
        (
            "cloose",
            dedent("""\
            Command not found. Did you mean:
              close"""),
        ),
        (
            "addd John 1234567890",
            dedent("""\
            Command not found. Did you mean:
              add John 1234567890
              add-note John 1234567890
              add-birthday John 1234567890"""),
        ),
        (
            "changee Name 123 456",
            dedent("""\
            Command not found. Did you mean:
              change Name 123 456
              phone Name 123 456"""),
        ),
        (
            "showw-birthday Name",
            dedent("""\
            Command not found. Did you mean:
              all
              birthdays
              show-birthday Name
              phone Name"""),
        ),
        (
            "alll",
            dedent("""\
            Command not found. Did you mean:
              all"""),
        ),
        (
            "birthdayss",
            dedent("""\
            Command not found. Did you mean:
              birthdays
              add-birthday Name 01.01.1990
              show-birthday Name"""),
        ),
        (
            "phonne Name",
            dedent("""\
            Command not found. Did you mean:
              phone Name
              change Name"""),
        ),
        (
            "helloo ",
            dedent("""\
            Command not found. Did you mean:
              hello"""),
        ),
    )

    with mock_data_io(book) as (mock_save, mock_load):
        commands = [command for command, _ in commands_to_response]
        expected = formatted_output(commands_to_response)

        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands), (book,))
