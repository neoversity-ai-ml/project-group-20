import os
import tempfile

from unittest.mock import patch
from tests.cli.helpers import run_cli, formatted_output
import pytest

from data_loading import load_data, save_data
from models import AddressBook
from main import main


def test_persisted_data(capsys, monkeypatch):
    try:
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name

        with (
            patch(
                "main.load_data",
                side_effect=lambda default_factory=AddressBook: load_data(
                    filename, default_factory
                ),
            ),
            patch("main.save_data", side_effect=lambda book: save_data(book, filename)),
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
            expected_output = formatted_output(commands_to_response)

            assert run_cli(commands, capsys, monkeypatch) == expected_output
    finally:
        os.remove(filename)


def test_no_data_file(capsys, monkeypatch):
    with tempfile.NamedTemporaryFile() as tmp:
        filename = tmp.name

    with (
        patch(
            "main.load_data",
            side_effect=lambda default_factory: load_data(filename, None),
        ),
        patch("main.save_data", side_effect=lambda book: save_data(book, filename)),
    ):
        with pytest.raises(FileNotFoundError):
            main()
