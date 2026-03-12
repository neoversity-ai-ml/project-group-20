import builtins
from contextlib import contextmanager
from typing import Iterable, Generator, Tuple

from unittest.mock import patch, MagicMock
from pytest import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from models import AddressBook
from main import main


@contextmanager
def mock_data_io(book: AddressBook) -> Generator[Tuple[MagicMock, MagicMock], None, None]:
    with (
        patch("main.save_data") as mock_save,
        patch("main.load_data", return_value=book) as mock_load,
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
        except StopIteration:
            raise EOFError

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
