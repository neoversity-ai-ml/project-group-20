import os
import tempfile
from unittest.mock import patch

import pytest
from helpers import formatted_output, run_cli

from address_book_bot.data_loading import load_data, save_data
from address_book_bot.main import main
from address_book_bot.models import AddressBook


def test_persisted_data(capsys, monkeypatch):
    try:
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name

        with (
            patch(
                "address_book_bot.main.load_data",
                side_effect=lambda default_factory=AddressBook: load_data(filename, default_factory),
            ),
            patch(
                "address_book_bot.main.save_data",
                side_effect=lambda book: save_data(book, filename),
            ),
        ):
            commands_to_response = (
                ("hello", "How can I help you?"),
                ("add John 1234567890", "Contact added."),
                ("exit", "Good bye!"),
            )
            commands = [command for command, _ in commands_to_response]
            expected_output = formatted_output(commands_to_response)

            assert run_cli(commands, capsys, monkeypatch) == expected_output

            commands_to_response = (
                ("all", "Contact name: John, phones: 1234567890"),
                ("close", "Good bye!"),
            )
            commands = [command for command, _ in commands_to_response]
            expected_output = formatted_output(commands_to_response, prefix="Welcome to the assistant bot!")

            assert run_cli(commands, capsys, monkeypatch) == expected_output
    finally:
        os.remove(filename)


def test_no_data_file(capsys, monkeypatch):
    with tempfile.NamedTemporaryFile() as tmp:
        filename = tmp.name

    with (
        patch(
            "address_book_bot.main.load_data",
            side_effect=lambda default_factory: load_data(filename, None),
        ),
        patch(
            "address_book_bot.main.save_data",
            side_effect=lambda book: save_data(book, filename),
        ),
    ):
        with pytest.raises(FileNotFoundError):
            main()
