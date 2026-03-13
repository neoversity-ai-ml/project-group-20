import textwrap

from helpers import run_cli, mock_data_io, assert_mock_called_n_times_with

from address_book_bot.models import AddressBook


def test_regexp_resolved_commands(capsys, monkeypatch):
    book = AddressBook()

    commands = (
        "hi",
        "Hey",
        "привіт",
        "heyy",
        "quit",
        "break",
        "quitt",
        "insert",
        "create",
        "Insert ",
        "edit",
        "modify",
        "eDit  ",
        "del",
        "delete",
        "remove",
        " del  ",
        "show",
        "display",
        "list",
        "birth",
        "day",
        "find",
        "call",
        "number",
    )

    expected = textwrap.dedent("""\
        Welcome to the assistant bot!
        Command not found. Did you mean:
          hello
        Command not found. Did you mean:
          hello
        Command not found. Did you mean:
          hello
        Command not found. Did you mean:
          hello
        Command not found. Did you mean:
          exit
          close
        Command not found. Did you mean:
          exit
          close
        Command not found. Did you mean:
          exit
          close
        Command not found. Did you mean:
          add Name 1234567890
          add-birthday Name 01.01.1990
        Command not found. Did you mean:
          add Name 1234567890
          add-birthday Name 01.01.1990
        Command not found. Did you mean:
          add Name 1234567890
          add-birthday Name 01.01.1990
        Command not found. Did you mean:
          change Name 1234567890 1234567891
          add-birthday Name 01.01.1990
        Command not found. Did you mean:
          change Name 1234567890 1234567891
          add-birthday Name 01.01.1990
        Command not found. Did you mean:
          change Name 1234567890 1234567891
          add-birthday Name 01.01.1990
        Command not found. Did you mean:
          delete contact
          delete birthday
        Command not found. Did you mean:
          delete contact
          delete birthday
        Command not found. Did you mean:
          delete contact
          delete birthday
        Command not found. Did you mean:
          delete contact
          delete birthday
        Command not found. Did you mean:
          all
          birthdays
          show-birthday Name
          phone Name
        Command not found. Did you mean:
          all
          birthdays
          show-birthday Name
          phone Name
        Command not found. Did you mean:
          all
          birthdays
          show-birthday Name
          phone Name
        Command not found. Did you mean:
          birthdays
          add-birthday Name 01.01.1990
          show-birthday Name
        Command not found. Did you mean:
          birthdays
          add-birthday Name 01.01.1990
          show-birthday Name
        Command not found. Did you mean:
          phone Name
          change Name 1234567890 1234567891
        Command not found. Did you mean:
          phone Name
          change Name 1234567890 1234567891
        Command not found. Did you mean:
          phone Name
          change Name 1234567890 1234567891
    """)

    with mock_data_io(book) as (mock_save, mock_load):
        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands), (book,))


def test_fuzzy_resolved_commands(capsys, monkeypatch):
    book = AddressBook()

    commands = (
        "helloo",
        "HE LLO",
        "exittt",
        "cloose",
        "addd John 1234567890",
        "changee Name 123 456",
        "showw-birthday Name",
        "alll",
        "birthdayss",
        "phonne Name",
        "helloo",
    )

    expected = textwrap.dedent("""\
        Welcome to the assistant bot!
        Command not found. Did you mean:
          hello
        Command not found. Did you mean:
          phone LLO
          hello LLO
          change LLO
        Command not found. Did you mean:
          exit
        Command not found. Did you mean:
          close
        Command not found. Did you mean:
          add John 1234567890
          add-birthday John 1234567890
        Command not found. Did you mean:
          change Name 123 456
          phone Name 123 456
        Command not found. Did you mean:
          all
          birthdays
          show-birthday Name
          phone Name
        Command not found. Did you mean:
          all
        Command not found. Did you mean:
          birthdays
          add-birthday Name 01.01.1990
          show-birthday Name
        Command not found. Did you mean:
          phone Name
          change Name
        Command not found. Did you mean:
          hello
    """)

    with mock_data_io(book) as (mock_save, mock_load):
        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands), (book,))
