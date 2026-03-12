import re
from typing import Iterable


class CommandResolver:
    def __init__(self, commands: Iterable[tuple[str, tuple[str, ...]]]):
        self.commands = [
            (re.compile(pattern, re.IGNORECASE), result) for pattern, result in commands
        ]

    def resolve(self, text: str) -> list[str] | None:
        text = text.lower().strip()

        for pattern, commands in self.commands:
            if pattern.search(text):
                return commands

        return None
