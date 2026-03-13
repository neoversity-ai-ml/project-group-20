from address_book_bot.data_loading import load_data, save_data
from address_book_bot.models import AddressBook
from address_book_bot.utils import parse_input
from address_book_bot.commands.commands import COMMANDS, DESCRIPTION_TEXT, suggest_command


def main():
    """Main function to run the assistant bot."""

    book = load_data(default_factory=AddressBook)
    print("Welcome to the assistant bot!")

    if len(book) == 0:
        print(DESCRIPTION_TEXT)

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in {"close", "exit"}:
            print("Good bye!")
            break

        handler = COMMANDS.get(command)

        if handler:
            print(handler(args, book))
        else:
            fallbacks = suggest_command(user_input, command, args)
            if fallbacks:
                print("Command not found. Did you mean:")
                for fallback in fallbacks:
                    print(f"  {fallback}")
            else:
                print("Invalid command.")

        save_data(book)


if __name__ == "__main__":  # pragma: no cover
    main()
