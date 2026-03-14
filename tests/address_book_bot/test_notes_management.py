from textwrap import dedent

from helpers import (
    assert_mock_called_n_times_with,
    formatted_output,
    mock_data_io,
    run_cli,
)

from address_book_bot.models import AddressBook


def test_notes_management(capsys, monkeypatch):
    book = AddressBook()

    commands_to_response = (
        ("add-note Python is a language.", "Note added."),
        ("add-note Python Python Python! Learning Python is fun. Best Python course.", "Note added."),
        ("add-note My homework з програмування на Python almost done.", "Note added."),
        ("add-note Bye.", "Note added."),
        (
            "show-notes",
            dedent("""\
                1. Python is a language.
                2. Python Python Python! Learning Python is fun. Best Python course.
                3. My homework з програмування на Python almost done.
                4. Bye."""),
        ),
        (
            "sort-notes",
            dedent("""\
                1. [bye] Bye.
                2. [homework, програмування, python] My homework з програмування на Python almost done.
                3. [python, learning, fun] Python Python Python! Learning Python is fun. Best Python course.
                4. [python, language] Python is a language."""),
        ),
        (
            "search-tag python",
            dedent("""\
                Python Python Python! Learning Python is fun. Best Python course.
                My homework з програмування на Python almost done.
                Python is a language."""),
        ),
        ("search bye", "Bye."),
        ("delete-note 3", "Note deleted."),
        ("edit-note 1 goodbye!", "Note updated."),
        (
            "show-notes",
            dedent("""\
                1. goodbye!
                2. My homework з програмування на Python almost done.
                3. Python is a language."""),
        ),
        ("exit", "Good bye!"),
    )

    with mock_data_io(book) as (mock_save, mock_load):
        commands = [command for command, _ in commands_to_response]
        expected = formatted_output(commands_to_response)

        assert run_cli(commands, capsys, monkeypatch) == expected

        mock_load.assert_called_once_with(default_factory=AddressBook)
        assert_mock_called_n_times_with(mock_save, len(commands) - 1, (book,))
