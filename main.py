from data_loading import load_data, save_data
from models import AddressBook, Record

from command_resolver import CommandResolver
from fuzzy_command_resolver import FuzzyCommandResolver


def input_error(func):
    """Decorator to handle common input errors."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format. Please provide all necessary arguments."

    return inner


def parse_input(user_input):
    """Parses user input into a command and arguments."""
    cmd, *args = user_input.split()
    return cmd.lower(), *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    raise KeyError


@input_error
def show_phone(args, book: AddressBook):
    (name,) = args
    record = book.find(name)
    if record:
        return "; ".join(p.value for p in record.phones)
    raise KeyError


def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    raise KeyError


@input_error
def show_birthday(args, book: AddressBook):
    (name,) = args
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    if record:
        return "Birthday not set for this contact."
    raise KeyError


@input_error
def birthdays(args, book: AddressBook):
    """Shows contacts with birthdays in the upcoming week."""

    if len(args) != 1 or not args[0].isdigit():
        raise ValueError(
            "Please provide the number of days to check for upcoming birthdays."
        )

    (days,) = args
    days = int(days)

    if days <= 0 or days > 365:
        raise ValueError("Days must be a positive number and not exceed 365.")

    birthdays_by_day = book.get_upcoming_birthdays(days)
    if not birthdays_by_day:
        return "No upcoming birthdays during requested period."

    output = []
    for entry in birthdays_by_day:
        d = entry["congratulation_date"]
        output.append(f"{d.strftime('%d.%m.%Y')} {entry['name']} ({d.strftime('%A')})")

    return (
        "\n".join(output) if output else "No upcoming birthdays during requested period."
    )


@input_error
def add_address(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Please provide name and address: name address.")

    name, address = args
    record = book.find(name)
    if record:
        record.add_address(address)
        return "Address added."
    raise KeyError


@input_error
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return "Email added."
    raise KeyError


@input_error
def show_email(args, book: AddressBook):
    (name,) = args
    record = book.find(name)

    if record:
        email = record.email or "Email not set for this contact."
        return email
    raise KeyError


command_resolver = CommandResolver(
    [
        (r"hi|hey|привіт", ("hello",)),
        (r"quit|break", ("exit", "close")),
        (r"insert|create", ("add Name 1234567890", "add-birthday Name 01.01.1990")),
        (
            r"edit|modify",
            ("change Name 1234567890 1234567891", "add-birthday Name 01.01.1990"),
        ),
        (r"del|delete|remove", ("delete contact", "delete birthday")),
        (r"show|display|list", ("all", "birthdays", "show-birthday Name", "phone Name")),
        (
            r"birth|day",
            ("birthdays", "add-birthday Name 01.01.1990", "show-birthday Name"),
        ),
        (r"find|call|number", ("phone Name", "change Name 1234567890 1234567891")),
    ]
)


fuzzy_resolver = FuzzyCommandResolver(
    {
        "hello": "hello",
        "exit": "exit",
        "close": "close",
        "add": "add Name 1234567890",
        "add-birthday": "add-birthday Name 01.01.1990",
        "change": "change Name 1234567890 1234567891",
        "show-birthday": "show-birthday Name",
        "all": "all",
        "birthdays": "birthdays",
        "phone": "phone Name",
    }
)


def main():
    """Main function to run the assistant bot."""

    book = load_data(default_factory=AddressBook)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "email":
            print(add_email(args, book))
        elif command == "show-email":
            print(show_email(args, book))
        else:
            fallbacks = (
                command_resolver.resolve(user_input)
                or fuzzy_resolver.resolve(command.lower(), args)
                or fuzzy_resolver.resolve(user_input, [])
            )
            if fallbacks:
                print("Command not found. Did you mean:")
                for fallback in fallbacks:
                    print(f"  {fallback}")
            else:
                print("Invalid command.")

        save_data(book)


if __name__ == "__main__":
    main()
