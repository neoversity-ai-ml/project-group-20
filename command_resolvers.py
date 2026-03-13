import re
from difflib import get_close_matches
from typing import Iterable


class CommandResolver:
    def __init__(self, commands: Iterable[tuple[str, tuple[str, ...]]]):
        self.commands = [
            (re.compile(pattern, re.IGNORECASE), result) for pattern, result in commands
        ]

    def resolve(self, text: str) -> list[str] | None:
        text = text.lower().strip()

        return next(
            (commands for pattern, commands in self.commands if pattern.search(text)),
            None,
        )


class FuzzyCommandResolver:
    def __init__(self, commands: dict[str, str], count: int = 5, cutoff: float = 0.5):
        self.keys = list(commands)
        self.commands = commands
        self.count = count
        self.cutoff = cutoff

    def resolve(self, text: str, suffix: list[str]) -> list[str]:
        matches = get_close_matches(text, self.keys, n=self.count, cutoff=self.cutoff)
        if suffix:
            return [f"{match} {' '.join(suffix)}" for match in matches]
        else:
            return [self.commands[match] for match in matches]
