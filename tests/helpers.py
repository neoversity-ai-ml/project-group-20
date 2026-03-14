import builtins
from collections.abc import Generator, Iterable
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from _pytest.monkeypatch import MonkeyPatch
from pytest import CaptureFixture

from address_book_bot.commands.commands import DESCRIPTION_TEXT
from address_book_bot.main import main
from address_book_bot.models import AddressBook


@contextmanager
def mock_data_io(book: AddressBook) -> Generator[tuple[MagicMock, MagicMock]]:
    with (
        patch("address_book_bot.main.save_data") as mock_save,
        patch("address_book_bot.main.load_data", return_value=book) as mock_load,
    ):
        yield mock_save, mock_load  # mock_save: MagicMock, mock_load: MagicMock


def run_cli(
    inputs: Iterable[str],
    capsys: CaptureFixture[str],
    monkeypatch: MonkeyPatch,
) -> str:
    commands = iter(inputs)

    def fake_input(prompt: str = "") -> str:
        try:
            return next(commands)
        except StopIteration as err:
            raise EOFError from err

    monkeypatch.setattr(builtins, "input", fake_input)

    try:
        main()
    except EOFError:
        pass

    return capsys.readouterr().out


def assert_mock_called_n_times_with(mock, n, arg):
    assert mock.call_count == n
    for call in mock.call_args_list:
        args, kwargs = call
        assert args == arg


def formatted_output(
    mapping: tuple[tuple[str, str | None], ...],
    prefix: str = f"Welcome to the assistant bot!\n{DESCRIPTION_TEXT}",
) -> str:
    output = "\n".join([response for _command, response in mapping if response is not None])
    output = f"{prefix}\n{output}\n" if prefix else f"{output}\n"
    return output
