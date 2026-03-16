from address_book_bot.commands.commands import COMMANDS, suggest_command
from address_book_bot.data_loading import load_data, save_data
from address_book_bot.models import AddressBook
from address_book_bot.ui import console, print_commands_table, print_error, print_info, print_success
from address_book_bot.utils import parse_input

_ERROR_PHRASES = ("not found", "invalid", "please provide", "cannot", "must be", "already")


def _is_error(msg: str) -> bool:
    return any(phrase in msg.lower() for phrase in _ERROR_PHRASES)


def main():
    """Main function to run the assistant bot."""

    book = load_data(default_factory=AddressBook)
    console.print("[bold cyan]Welcome to the assistant bot![/bold cyan]")
    print_commands_table()

    while True:
        user_input = input("\nEnter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in {"close", "exit"}:
            console.print("[bold cyan]Good bye![/bold cyan]")
            break

        handler = COMMANDS.get(command)

        if handler:
            result = handler(args, book)
            if result:
                (print_error if _is_error(result) else print_success)(result)
            save_data(book)
        else:
            fallbacks = suggest_command(user_input, command, args)
            if fallbacks:
                print_info("Command not found. Did you mean:")
                for fallback in fallbacks:
                    print_info(f"  {fallback}")
            else:
                print_error("Invalid command.")


if __name__ == "__main__":  # pragma: no cover
    main()
