from difflib import get_close_matches


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
